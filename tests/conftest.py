"""
Shared fixtures and configuration for all tests.
"""
import os
import pytest
import json
from unittest.mock import MagicMock, patch
from datetime import timedelta

# Set environment variables before importing the app
os.environ.setdefault("MYSQL_USER", "test_user")
os.environ.setdefault("MYSQL_PASSWORD", "test_password")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "3306")
os.environ.setdefault("MYSQL_DATABASE", "test_db")
os.environ.setdefault("ALLOWED_ORIGINS", "http://localhost:3000")
os.environ.setdefault("REDIS_HOST", "localhost")
os.environ.setdefault("REDIS_PORT", "6379")
os.environ.setdefault("REDIS_PASSWORD", "")


@pytest.fixture
def mock_redis():
    """Mock Redis client"""
    with patch("src.customer_service.extentions.redis_client.redis_client") as mock:
        mock.get = MagicMock()
        mock.set = MagicMock()
        mock.delete = MagicMock()
        yield mock


@pytest.fixture
def mock_db():
    """Mock SQLAlchemy database"""
    with patch("src.customer_service.extentions.db.db") as mock:
        mock.session = MagicMock()
        mock.create_all = MagicMock()
        yield mock


@pytest.fixture
def app_with_context(mock_db, mock_redis):
    """Create Flask app for testing with mocked database"""
    from src.customer_service.main import create_app
    
    app = create_app(db_url="sqlite:///:memory:")
    
    # Override the actual db and redis with mocks
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "test_secret_key"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    
    return app


@pytest.fixture
def app_context(app_with_context):
    """App application context"""
    with app_with_context.app_context():
        yield app_with_context


@pytest.fixture
def client(app_context):
    """Test client"""
    return app_context.test_client()


@pytest.fixture
def sample_customer_data():
    """Sample valid customer data"""
    return {
        "customer_no": "CUST001",
        "name": "Test Customer",
        "explicit_ext_ref": "EXT_REF_001",
        "abn": "12345678901234",
        "order_no_recycle_days": 30,
        "shipment_days": "1-5",
        "cancel_order_days": 10,
        "gtin_interpretation": 1,
        "retailer_customisation_format": 1,
        "share_retailer_values": 1,
        "perform_retailer_validation": 1,
        "perform_trade_units_validation": 0,
        "perform_pack_sizes_validation": 0,
        "perform_pallets_validation": 0,
        "allow_change_order": 1,
        "allow_back_order": 1,
        "allow_delivery_dates_change": 1,
        "allow_part_shipment": 1,
        "allow_over_shipment": 1,
        "allow_reject_order": 1,
        "allow_allowances": 1,
        "allow_pack_size_change": 1,
        "allow_hand_pick": 1,
        "allow_over_pick": 1,
        "allow_pick_by_prod_wo_scan": 1,
    }


@pytest.fixture
def valid_token():
    """Generate a valid test JWT token"""
    from flask_jwt_extended import create_access_token
    return create_access_token(identity=1)


@pytest.fixture
def expired_token():
    """Generate an expired JWT token"""
    from flask_jwt_extended import create_access_token
    from datetime import timedelta, datetime, timezone
    
    # Create a token with very short expiration
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime.now(timezone.utc) - timedelta(hours=2)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        # In real scenario, use an old token
    
    return create_access_token(identity=1, expires_delta=timedelta(seconds=-1))


@pytest.fixture
def redis_session(mock_redis):
    """Mock a valid Redis session"""
    def _set_session(user_id, token):
        session_data = {
            "token": token,
            "user_id": user_id,
            "created_at": "2024-01-01T00:00:00"
        }
        mock_redis.get.return_value = json.dumps(session_data)
        return session_data
    
    return _set_session


@pytest.fixture
def headers_with_token(valid_token):
    """Headers with valid JWT token"""
    return {"Authorization": f"Bearer {valid_token}"}
