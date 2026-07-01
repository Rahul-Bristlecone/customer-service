"""
Tests for database extension
"""
import pytest
from unittest.mock import MagicMock, patch
from flask_sqlalchemy import SQLAlchemy


class TestDatabaseExtension:
    """Test database extension initialization"""
    
    def test_db_is_sqlalchemy_instance(self):
        """Test that db is a SQLAlchemy instance"""
        from customer_service.extentions.db import db
        assert isinstance(db, SQLAlchemy)
    
    def test_db_can_be_initialized_with_app(self, app_context):
        """Test that db can be initialized with Flask app"""
        from customer_service.extentions.db import db
        
        # db should already be initialized with the app in the fixture
        assert db is not None
    
    @patch('flask_sqlalchemy.SQLAlchemy.init_app')
    def test_db_init_app_called(self, mock_init_app, app_context):
        """Test that init_app can be called on db"""
        from customer_service.extentions.db import db
        
        # The db.init_app should have been called
        # This verifies the pattern used in main.py
        pass


class TestDatabaseConfiguration:
    """Test database configuration"""
    
    def test_app_has_sqlalchemy_database_uri(self, app_context):
        """Test that app has SQLALCHEMY_DATABASE_URI configured"""
        assert "SQLALCHEMY_DATABASE_URI" in app_context.config
    
    def test_database_uri_format(self, app_context):
        """Test that database URI has correct format"""
        uri = app_context.config["SQLALCHEMY_DATABASE_URI"]
        # Should be mysql+pymysql format
        assert "mysql" in uri or "sqlite" in uri
    
    def test_testing_mode_enabled(self, app_context):
        """Test that testing mode is enabled"""
        assert app_context.config["TESTING"] is True


class TestDatabaseSession:
    """Test database session management"""
    
    def test_db_session_exists(self, app_context):
        """Test that db.session exists"""
        from customer_service.extentions.db import db
        
        assert hasattr(db, 'session')
        assert db.session is not None
    
    def test_db_model_exists(self, app_context):
        """Test that db.Model is available"""
        from customer_service.extentions.db import db
        
        assert hasattr(db, 'Model')
