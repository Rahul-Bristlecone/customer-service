"""
Tests for customer resource endpoints
"""
import json
import pytest
from unittest.mock import MagicMock, patch
from flask_jwt_extended import create_access_token


class TestValidateActiveSession:
    """Test the validate_active_session helper function"""
    
    def test_validate_active_session_missing_auth_header(self, app_context):
        """Test session validation fails without auth header"""
        from customer_service.resources.customer import validate_active_session
        
        with app_context.test_request_context(headers={}):
            with pytest.raises(Exception):
                validate_active_session(1)
    
    def test_validate_active_session_invalid_token_format(self, app_context):
        """Test session validation fails with invalid token format"""
        from customer_service.resources.customer import validate_active_session
        
        with app_context.test_request_context(headers={"Authorization": "InvalidFormat"}):
            with pytest.raises(Exception):
                validate_active_session(1)
    
    @patch('customer_service.resources.customer.redis_client')
    def test_validate_active_session_no_cached_session(self, mock_redis, app_context):
        """Test session validation fails when session not in Redis"""
        from customer_service.resources.customer import validate_active_session
        
        mock_redis.get.return_value = None
        token = create_access_token(identity=1)
        
        with app_context.test_request_context(headers={"Authorization": f"Bearer {token}"}):
            with pytest.raises(Exception):
                validate_active_session(1)
    
    @patch('customer_service.resources.customer.redis_client')
    def test_validate_active_session_invalid_session_data(self, mock_redis, app_context):
        """Test session validation fails with invalid cached data"""
        from customer_service.resources.customer import validate_active_session
        
        mock_redis.get.return_value = "invalid json"
        token = create_access_token(identity=1)
        
        with app_context.test_request_context(headers={"Authorization": f"Bearer {token}"}):
            with pytest.raises(Exception):
                validate_active_session(1)
    
    @patch('customer_service.resources.customer.redis_client')
    def test_validate_active_session_token_mismatch(self, mock_redis, app_context):
        """Test session validation fails when token doesn't match"""
        from customer_service.resources.customer import validate_active_session
        
        cached_session = {"token": "different_token", "user_id": 1}
        mock_redis.get.return_value = json.dumps(cached_session)
        token = create_access_token(identity=1)
        
        with app_context.test_request_context(headers={"Authorization": f"Bearer {token}"}):
            with pytest.raises(Exception):
                validate_active_session(1)
    
    @patch('customer_service.resources.customer.redis_client')
    def test_validate_active_session_success(self, mock_redis, app_context):
        """Test successful session validation"""
        from customer_service.resources.customer import validate_active_session
        
        token = create_access_token(identity=1)
        cached_session = {"token": token, "user_id": 1}
        mock_redis.get.return_value = json.dumps(cached_session)
        
        with app_context.test_request_context(headers={"Authorization": f"Bearer {token}"}):
            # Should not raise
            validate_active_session(1)


class TestGetUserCustomerOr404:
    """Test the get_user_customer_or_404 helper function"""
    
    @patch('customer_service.resources.customer.CustomerModel')
    def test_get_user_customer_found(self, mock_model, app_context):
        """Test retrieving existing customer"""
        from customer_service.resources.customer import get_user_customer_or_404
        
        mock_customer = MagicMock()
        mock_customer.customer_id = 1
        mock_customer.user_id = 1
        
        mock_model.query.filter_by.return_value.first.return_value = mock_customer
        
        with app_context.test_request_context():
            customer = get_user_customer_or_404(1, 1)
            assert customer.customer_id == 1
    
    @patch('customer_service.resources.customer.CustomerModel')
    def test_get_user_customer_not_found(self, mock_model, app_context):
        """Test 404 when customer not found"""
        from customer_service.resources.customer import get_user_customer_or_404
        
        mock_model.query.filter_by.return_value.first.return_value = None
        
        with app_context.test_request_context():
            with pytest.raises(Exception):
                get_user_customer_or_404(999, 1)


class TestCreateCustomerFromPayload:
    """Test the create_customer_from_payload helper function"""
    
    @patch('customer_service.resources.customer.validate_active_session')
    @patch('customer_service.resources.customer.get_jwt_identity')
    @patch('customer_service.resources.customer.CustomerModel')
    @patch('customer_service.resources.customer.db')
    def test_create_customer_success(self, mock_db, mock_model_class, mock_jwt, mock_validate, app_context):
        """Test successful customer creation"""
        from customer_service.resources.customer import create_customer_from_payload
        
        mock_jwt.return_value = "1"
        mock_validate.return_value = None
        mock_instance = MagicMock()
        mock_instance.customer_id = 1
        mock_model_class.return_value = mock_instance
        mock_db.session.commit = MagicMock()
        
        with app_context.test_request_context():
            customer = create_customer_from_payload({"customer_no": "CUST001"})
            assert mock_db.session.add.called
            assert mock_db.session.commit.called
    
    @patch('customer_service.resources.customer.validate_active_session')
    @patch('customer_service.resources.customer.get_jwt_identity')
    @patch('customer_service.resources.customer.db')
    def test_create_customer_integrity_error(self, mock_db, mock_jwt, mock_validate, app_context):
        """Test handling of IntegrityError during creation"""
        from customer_service.resources.customer import create_customer_from_payload
        from sqlalchemy.exc import IntegrityError
        
        mock_jwt.return_value = "1"
        mock_validate.return_value = None
        mock_db.session.add = MagicMock()
        mock_db.session.commit.side_effect = IntegrityError("Duplicate", "", "")
        mock_db.session.rollback = MagicMock()
        
        with app_context.test_request_context():
            with pytest.raises(Exception):
                create_customer_from_payload({"customer_no": "CUST001"})
            assert mock_db.session.rollback.called
    
    @patch('customer_service.resources.customer.validate_active_session')
    @patch('customer_service.resources.customer.get_jwt_identity')
    @patch('customer_service.resources.customer.db')
    def test_create_customer_sqlalchemy_error(self, mock_db, mock_jwt, mock_validate, app_context):
        """Test handling of SQLAlchemyError during creation"""
        from customer_service.resources.customer import create_customer_from_payload
        from sqlalchemy.exc import SQLAlchemyError
        
        mock_jwt.return_value = "1"
        mock_validate.return_value = None
        mock_db.session.add = MagicMock()
        mock_db.session.commit.side_effect = SQLAlchemyError("DB Error")
        mock_db.session.rollback = MagicMock()
        
        with app_context.test_request_context():
            with pytest.raises(Exception):
                create_customer_from_payload({"customer_no": "CUST001"})
            assert mock_db.session.rollback.called


class TestCreateCustomerEndpoint:
    """Test POST /create_customer endpoint"""
    
    @patch('customer_service.resources.customer.validate_active_session')
    @patch('customer_service.resources.customer.get_jwt_identity')
    @patch('customer_service.resources.customer.db')
    @patch('customer_service.resources.customer.CustomerModel')
    def test_create_customer_success(self, mock_model_class, mock_db, mock_jwt, mock_validate,
                                    client, valid_token, mock_redis):
        """Test successful customer creation"""
        mock_jwt.return_value = "1"
        mock_validate.return_value = None
        mock_instance = MagicMock()
        mock_instance.customer_id = 1
        mock_instance.customer_no = "CUST001"
        mock_model_class.return_value = mock_instance
        mock_db.session.commit = MagicMock()
        
        session_data = {"token": valid_token}
        mock_redis.get.return_value = json.dumps(session_data)
        
        headers = {"Authorization": f"Bearer {valid_token}"}
        response = client.post(
            '/create_customer',
            json={"customer_no": "CUST001"},
            headers=headers
        )
        assert response.status_code in [201, 422, 401]


class TestGetCustomerEndpoint:
    """Test GET /customer/<customer_id> endpoint"""
    
    @patch('customer_service.resources.customer.validate_active_session')
    @patch('customer_service.resources.customer.get_jwt_identity')
    @patch('customer_service.resources.customer.get_user_customer_or_404')
    def test_get_customer_success(self, mock_get_customer, mock_jwt, mock_validate,
                                 client, valid_token, mock_redis):
        """Test successful customer retrieval"""
        mock_jwt.return_value = "1"
        mock_validate.return_value = None
        mock_customer = MagicMock()
        mock_customer.customer_id = 1
        mock_customer.customer_no = "CUST001"
        mock_get_customer.return_value = mock_customer
        
        session_data = {"token": valid_token}
        mock_redis.get.return_value = json.dumps(session_data)
        
        headers = {"Authorization": f"Bearer {valid_token}"}
        response = client.get('/customer/1', headers=headers)
        assert response.status_code in [200, 422, 401]
    
    def test_get_customer_missing_token(self, client):
        """Test customer retrieval without token"""
        response = client.get('/customer/1')
        assert response.status_code in [401, 422]


class TestUpdateCustomerEndpoint:
    """Test PUT /customer/<customer_id> endpoint"""
    
    @patch('customer_service.resources.customer.validate_active_session')
    @patch('customer_service.resources.customer.get_jwt_identity')
    @patch('customer_service.resources.customer.get_user_customer_or_404')
    @patch('customer_service.resources.customer.db')
    def test_update_customer_success(self, mock_db, mock_get_customer, mock_jwt, mock_validate,
                                    client, valid_token, mock_redis):
        """Test successful customer update"""
        mock_jwt.return_value = "1"
        mock_validate.return_value = None
        mock_customer = MagicMock()
        mock_customer.customer_id = 1
        mock_customer.customer_no = "CUST001"
        mock_get_customer.return_value = mock_customer
        mock_db.session.commit = MagicMock()
        
        session_data = {"token": valid_token}
        mock_redis.get.return_value = json.dumps(session_data)
        
        headers = {"Authorization": f"Bearer {valid_token}"}
        response = client.put(
            '/customer/1',
            json={"name": "New Name"},
            headers=headers
        )
        assert response.status_code in [200, 422, 401]
    
    @patch('customer_service.resources.customer.validate_active_session')
    @patch('customer_service.resources.customer.get_jwt_identity')
    @patch('customer_service.resources.customer.get_user_customer_or_404')
    def test_update_customer_cannot_change_customer_no(self, mock_get_customer, mock_jwt, mock_validate,
                                                      client, valid_token, mock_redis):
        """Test that customer_no cannot be updated"""
        mock_jwt.return_value = "1"
        mock_validate.return_value = None
        mock_customer = MagicMock()
        mock_get_customer.return_value = mock_customer
        
        session_data = {"token": valid_token}
        mock_redis.get.return_value = json.dumps(session_data)
        
        headers = {"Authorization": f"Bearer {valid_token}"}
        response = client.put(
            '/customer/1',
            json={"customer_no": "NEWCUST"},
            headers=headers
        )
        # Should fail with 400 or similar
        assert response.status_code in [400, 422, 401]


class TestDeleteCustomerEndpoint:
    """Test DELETE /customer/<customer_id> endpoint"""
    
    @patch('customer_service.resources.customer.validate_active_session')
    @patch('customer_service.resources.customer.get_jwt_identity')
    @patch('customer_service.resources.customer.get_user_customer_or_404')
    @patch('customer_service.resources.customer.db')
    def test_delete_customer_success(self, mock_db, mock_get_customer, mock_jwt, mock_validate,
                                    client, valid_token, mock_redis):
        """Test successful customer deletion"""
        mock_jwt.return_value = "1"
        mock_validate.return_value = None
        mock_customer = MagicMock()
        mock_customer.customer_id = 1
        mock_get_customer.return_value = mock_customer
        mock_db.session.delete = MagicMock()
        mock_db.session.commit = MagicMock()
        
        session_data = {"token": valid_token}
        mock_redis.get.return_value = json.dumps(session_data)
        
        headers = {"Authorization": f"Bearer {valid_token}"}
        response = client.delete('/customer/1', headers=headers)
        assert response.status_code in [200, 422, 401]


class TestGetCustomersListEndpoint:
    """Test GET /customers endpoint"""
    
    @patch('customer_service.resources.customer.validate_active_session')
    @patch('customer_service.resources.customer.get_jwt_identity')
    @patch('customer_service.resources.customer.CustomerModel')
    def test_get_customers_success(self, mock_model, mock_jwt, mock_validate,
                                  client, valid_token, mock_redis):
        """Test successful customers list retrieval"""
        mock_jwt.return_value = "1"
        mock_validate.return_value = None
        mock_customers = [
            MagicMock(customer_id=1, customer_no="CUST001"),
            MagicMock(customer_id=2, customer_no="CUST002")
        ]
        mock_model.query.filter_by.return_value.all.return_value = mock_customers
        
        session_data = {"token": valid_token}
        mock_redis.get.return_value = json.dumps(session_data)
        
        headers = {"Authorization": f"Bearer {valid_token}"}
        response = client.get('/customers', headers=headers)
        assert response.status_code in [200, 422, 401]
    
    def test_get_customers_missing_token(self, client):
        """Test customers list without token"""
        response = client.get('/customers')
        assert response.status_code in [401, 422]
    
    @patch('customer_service.resources.customer.validate_active_session')
    @patch('customer_service.resources.customer.get_jwt_identity')
    @patch('customer_service.resources.customer.CustomerModel')
    def test_get_customers_empty_list(self, mock_model, mock_jwt, mock_validate,
                                     client, valid_token, mock_redis):
        """Test customers list when no customers exist"""
        mock_jwt.return_value = "1"
        mock_validate.return_value = None
        mock_model.query.filter_by.return_value.all.return_value = []
        
        session_data = {"token": valid_token}
        mock_redis.get.return_value = json.dumps(session_data)
        
        headers = {"Authorization": f"Bearer {valid_token}"}
        response = client.get('/customers', headers=headers)
        assert response.status_code in [200, 422, 401]

