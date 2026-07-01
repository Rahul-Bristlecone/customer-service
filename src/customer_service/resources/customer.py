import json
from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from customer_service.extentions.db import db
from customer_service.extentions.redis_client import redis_client
from customer_service.models.customer_model import CustomerModel
from customer_service.schemas.customer_schema import CustomerSchema

# Create blueprint for Customers
blp = Blueprint("customers", __name__, description="Operations on customers")


def validate_active_session(user_id):
    """Validate user session from Redis cache and JWT token"""
    auth_header = request.headers.get("Authorization", "")
    token_parts = auth_header.split()
    if len(token_parts) != 2:
        abort(401, message="Missing or invalid authorization token")

    token = token_parts[1]
    cached_session = redis_client.get(f"session:{user_id}")
    if not cached_session:
        abort(401, message="Session expired or revoked")

    try:
        session_data = json.loads(cached_session)
        cached_token = session_data.get("token")
    except Exception:
        abort(401, message="Invalid session data")

    if cached_token != token:
        abort(401, message="Session expired or revoked")


def get_user_customer_or_404(customer_id, user_id):
    """Get customer by ID and user_id, or return 404"""
    customer = CustomerModel.query.filter_by(customer_id=customer_id, user_id=user_id).first()
    if not customer:
        abort(404, message="Customer not found")
    return customer


def create_customer_from_payload(customer_data):
    """
    Shared logic to create a customer in the database.
    Validates JWT, checks Redis session, and persists the customer.
    """
    user_id = int(get_jwt_identity())
    validate_active_session(user_id)

    # Inject user_id from JWT
    customer = CustomerModel(user_id=user_id, **customer_data)

    try:
        db.session.add(customer)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, message="Customer number already exists for this user")
    except SQLAlchemyError:
        db.session.rollback()
        abort(500, message="Error inserting customer into database")

    return customer


# -------------------------------
# Endpoint: /create_customer
# -------------------------------
@blp.route("/create_customer")
class CustomerCreate(MethodView):
    @jwt_required()
    @blp.arguments(CustomerSchema)
    @blp.response(201, CustomerSchema)
    def post(self, customer_data):
        return create_customer_from_payload(customer_data)


# -------------------------------
# Endpoint: /customer/<customer_id>
# -------------------------------
@blp.route("/customer/<int:customer_id>")
class CustomerResource(MethodView):
    @jwt_required()
    @blp.response(200, CustomerSchema)
    def get(self, customer_id):
        """Get a specific customer by ID"""
        user_id = int(get_jwt_identity())
        validate_active_session(user_id)
        customer = get_user_customer_or_404(customer_id, user_id)
        return customer

    @jwt_required()
    @blp.arguments(CustomerSchema(partial=True))
    @blp.response(200, CustomerSchema)
    def put(self, customer_data, customer_id):
        """Update a specific customer"""
        user_id = int(get_jwt_identity())
        validate_active_session(user_id)

        customer = get_user_customer_or_404(customer_id, user_id)

        # customer_no cannot be updated after creation
        if "customer_no" in customer_data:
            abort(400, message="customer_no cannot be updated")

        # Ensure customer ownership cannot be reassigned via request payload
        customer_data.pop("user_id", None)
        customer_data.pop("customer_id", None)

        for key, value in customer_data.items():
            setattr(customer, key, value)

        try:
            db.session.add(customer)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="Customer number already exists")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Error updating customer in database")

        return customer

    @jwt_required()
    def delete(self, customer_id):
        """Delete a specific customer"""
        user_id = int(get_jwt_identity())
        validate_active_session(user_id)

        customer = get_user_customer_or_404(customer_id, user_id)

        try:
            db.session.delete(customer)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Error deleting customer from database")

        return {"message": "Customer deleted successfully"}, 200


# -------------------------------
# Endpoint: /customers
# -------------------------------
@blp.route("/customers")
class CustomerList(MethodView):
    @jwt_required()
    @blp.response(200, CustomerSchema(many=True))
    def get(self):
        """Get all customers for the authenticated user"""
        user_id = int(get_jwt_identity())
        validate_active_session(user_id)
        return CustomerModel.query.filter_by(user_id=user_id).all()


# To upload customer data using csv or excel sheet
# @blp.route("/upload_customer_data")
# class UploadCustomerResource(MethodView):
#     @jwt_required()
#     @blp.response(201, CustomerSchema)
#     def post(self):
#         if "file" not in request.files:
#             abort(400, message="No file uploaded")
#
#         customer_file = request.files["file"]
#         file_path = os.path.join("/tmp", customer_file.filename)
#         customer_file.save(file_path)
#
#         # Transform csv data → JSON
#         customer_data = transform_csv_to_json(file_path)
#
#         # Reuse the same customer creation logic
#         return create_customer_from_payload(customer_data)
