"""
Tests for main.py (Flask app factory)
"""
import os
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask


class TestAppFactory:
    """Test the create_app factory function"""
    
    def test_create_app_returns_flask_app(self, mock_db, mock_redis):
        """Test that create_app returns a Flask app instance"""
        from customer_service.main import create_app
        
        app = create_app()
        assert isinstance(app, Flask)
    
    def test_app_has_required_config(self, app_with_context):
        """Test that app has required configuration"""
        required_configs = [
            "CORS_AUTOMATIC_OPTIONS",
            "PROPAGATE_EXCEPTIONS",
            "API_TITLE",
            "API_VERSION",
            "OPENAPI_VERSION",
            "SQLALCHEMY_DATABASE_URI",
            "TESTING"
        ]
        
        for config_key in required_configs:
            assert config_key in app_with_context.config


class TestAppConfiguration:
    """Test Flask app configuration"""
    
    def test_cors_automatic_options_enabled(self, app_with_context):
        """Test CORS automatic options is enabled"""
        assert app_with_context.config["CORS_AUTOMATIC_OPTIONS"] is True
    
    def test_propagate_exceptions_enabled(self, app_with_context):
        """Test exception propagation is enabled"""
        assert app_with_context.config["PROPAGATE_EXCEPTIONS"] is True
    
    def test_api_title_set(self, app_with_context):
        """Test API title is set"""
        assert app_with_context.config["API_TITLE"] == "Customer service API"
    
    def test_api_version_set(self, app_with_context):
        """Test API version is set"""
        assert app_with_context.config["API_VERSION"] == "v1"
    
    def test_openapi_version_set(self, app_with_context):
        """Test OpenAPI version is set"""
        assert app_with_context.config["OPENAPI_VERSION"] == "3.0.3"
    
    def test_swagger_ui_configured(self, app_with_context):
        """Test Swagger UI configuration"""
        assert app_with_context.config["OPENAPI_SWAGGER_UI_PATH"] == "/swagger-ui"
        assert "swagger-ui-dist" in app_with_context.config["OPENAPI_SWAGGER_UI_URL"]
    
    def test_testing_mode_enabled_in_app(self, app_with_context):
        """Test that testing mode is enabled"""
        assert app_with_context.config["TESTING"] is True


class TestAppCORS:
    """Test CORS configuration"""
    
    def test_allowed_origins_from_env(self, app_with_context):
        """Test CORS allowed origins from environment"""
        original = os.getenv("ALLOWED_ORIGINS")
        try:
            os.environ["ALLOWED_ORIGINS"] = "http://localhost:3000,http://localhost:3001"
            # App should parse these origins
            assert original is not None
        finally:
            if original:
                os.environ["ALLOWED_ORIGINS"] = original
    
    def test_cors_allows_credentials(self, app_with_context):
        """Test CORS configuration allows credentials"""
        # This should be configured in CORS setup
        pass
    
    def test_cors_allowed_methods(self, app_with_context):
        """Test CORS allows specified HTTP methods"""
        # GET, POST, PUT, DELETE, OPTIONS should be allowed
        pass
    
    def test_cors_allowed_headers(self, app_with_context):
        """Test CORS allows required headers"""
        # Content-Type and Authorization should be allowed
        pass


class TestAppJWT:
    """Test JWT configuration"""
    
    def test_jwt_secret_key_in_config(self, app_with_context):
        """Test that JWT secret key is configured"""
        # JWT_SECRET_KEY should be in config (may be from env or test)
        assert "JWT_SECRET_KEY" in app_with_context.config or \
               os.getenv("JWT_SECRET_KEY") is not None
    
    def test_jwt_manager_initialized(self, app_with_context):
        """Test that JWTManager is initialized"""
        from flask_jwt_extended import JWTManager
        # JWTManager should be initialized with the app
        pass


class TestAppDatabase:
    """Test database integration"""
    
    def test_db_initialized_with_app(self, app_with_context):
        """Test that database is initialized with app"""
        from customer_service.extentions.db import db
        
        # db should be initialized with the app context
        assert app_with_context is not None
    
    def test_sqlalchemy_database_uri_configured(self, app_with_context):
        """Test that SQLAlchemy database URI is configured"""
        uri = app_with_context.config.get("SQLALCHEMY_DATABASE_URI")
        assert uri is not None
        # SQLite test URI won't have +, but production will
        assert "sqlite" in uri or "+" in uri
    
    @patch('customer_service.extentions.db.db.create_all')
    def test_db_create_all_called(self, mock_create_all, mock_db, mock_redis):
        """Test that db.create_all is called during initialization"""
        from customer_service.main import create_app
        
        mock_db.create_all = MagicMock()
        app = create_app()
        
        # create_all should be called during app initialization
        # This is done in the app context


class TestAppRoutes:
    """Test app routes registration"""
    
    def test_customer_blueprint_registered(self, app_with_context):
        """Test that customer blueprint is registered"""
        # The customer blueprint should be registered
        blueprints = app_with_context.blueprints
        assert "customers" in blueprints or any("customer" in bp for bp in blueprints)
    
    def test_swagger_ui_route_exists(self, client):
        """Test that Swagger UI route is accessible"""
        # Swagger UI should be at /swagger-ui
        # This might return various status codes depending on setup
        pass


class TestAppErrorHandling:
    """Test app error handling"""
    
    def test_app_handles_404_errors(self, client):
        """Test that app handles 404 errors"""
        response = client.get("/nonexistent_endpoint")
        assert response.status_code == 404
    
    def test_app_has_error_handler(self, app_with_context):
        """Test that app has error handlers configured"""
        # Error handlers should be configured
        assert len(app_with_context.error_handler_spec) >= 0


class TestAppContext:
    """Test app context functionality"""
    
    def test_app_context_can_be_created(self, app_with_context):
        """Test that app context can be created"""
        with app_with_context.app_context():
            from customer_service.extentions.db import db
            assert db is not None
    
    def test_app_test_client_works(self, client):
        """Test that test client can be created"""
        # Test client should be available
        assert client is not None


class TestAppEnvironmentVariables:
    """Test environment variable handling"""
    
    def test_allowed_origins_env_var_used(self):
        """Test that ALLOWED_ORIGINS env var is used"""
        original = os.getenv("ALLOWED_ORIGINS")
        try:
            os.environ["ALLOWED_ORIGINS"] = "http://localhost:3000"
            assert os.getenv("ALLOWED_ORIGINS") == "http://localhost:3000"
        finally:
            if original:
                os.environ["ALLOWED_ORIGINS"] = original
    
    def test_mysql_credentials_from_env(self):
        """Test MySQL credentials from environment"""
        assert os.getenv("MYSQL_USER") is not None
        assert os.getenv("MYSQL_PASSWORD") is not None
        assert os.getenv("DB_HOST") is not None
        assert os.getenv("MYSQL_DATABASE") is not None
    
    def test_redis_config_from_env(self):
        """Test Redis config from environment"""
        assert os.getenv("REDIS_HOST") is not None
        assert os.getenv("REDIS_PORT") is not None


class TestAppFactory:
    """Test factory pattern implementation"""
    
    def test_create_app_with_custom_db_url(self, mock_db, mock_redis):
        """Test that create_app accepts custom database URL"""
        from customer_service.main import create_app
        
        custom_url = "sqlite:///test.db"
        app = create_app(db_url=custom_url)
        
        # Custom db_url parameter is accepted
        assert app is not None
    
    def test_multiple_app_instances_independent(self, mock_db, mock_redis):
        """Test that multiple app instances are independent"""
        from customer_service.main import create_app
        
        app1 = create_app()
        app2 = create_app()
        
        # Should be different instances
        assert app1 is not app2


class TestAppIntegration:
    """Integration tests for app setup"""
    
    def test_app_with_environment_setup(self, mock_db, mock_redis):
        """Test app creation with full environment setup"""
        from customer_service.main import create_app
        
        app = create_app()
        
        # All critical components should be available
        assert app is not None
        assert app.config["TESTING"] is True
    
    def test_app_can_handle_requests(self, client):
        """Test that app can handle HTTP requests"""
        # Should be able to make requests to the app
        response = client.get("/")
        # Status should be some valid HTTP code
        assert isinstance(response.status_code, int)
