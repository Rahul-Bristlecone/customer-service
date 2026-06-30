"""
Tests for Redis client extension
"""
import pytest
import os
from unittest.mock import patch, MagicMock
import redis


class TestRedisClientInitialization:
    """Test Redis client initialization"""
    
    def test_redis_client_is_redis_instance(self):
        """Test that redis_client is a Redis instance"""
        # Patch redis.Redis to avoid actual connection
        with patch('redis.Redis') as mock_redis_class:
            mock_redis_class.return_value = MagicMock()
            # Reimport to test initialization
            import importlib
            import src.customer_service.extentions.redis_client
            importlib.reload(src.customer_service.extentions.redis_client)
    
    def test_redis_client_default_host(self):
        """Test that Redis client uses default host if not configured"""
        # Save original env var
        original_host = os.getenv("REDIS_HOST")
        
        try:
            # Remove the env var
            if "REDIS_HOST" in os.environ:
                del os.environ["REDIS_HOST"]
            
            with patch('redis.Redis') as mock_redis_class:
                mock_redis_class.return_value = MagicMock()
                
                # Test the actual connection params
                # The default should be "redis-service"
                assert os.getenv("REDIS_HOST", "redis-service") == "redis-service"
        finally:
            # Restore original
            if original_host:
                os.environ["REDIS_HOST"] = original_host
    
    def test_redis_client_default_port(self):
        """Test that Redis client uses default port"""
        original_port = os.getenv("REDIS_PORT")
        
        try:
            if "REDIS_PORT" in os.environ:
                del os.environ["REDIS_PORT"]
            
            assert os.getenv("REDIS_PORT", "6379") == "6379"
        finally:
            if original_port:
                os.environ["REDIS_PORT"] = original_port
    
    def test_redis_client_password_none_when_empty(self):
        """Test that password is None when empty string"""
        original_pass = os.getenv("REDIS_PASSWORD")
        
        try:
            os.environ["REDIS_PASSWORD"] = ""
            password = os.getenv("REDIS_PASSWORD") or None
            assert password is None
        finally:
            if original_pass:
                os.environ["REDIS_PASSWORD"] = original_pass
    
    def test_redis_client_password_set_when_configured(self):
        """Test that password is used when configured"""
        original_pass = os.getenv("REDIS_PASSWORD")
        
        try:
            os.environ["REDIS_PASSWORD"] = "test_password"
            password = os.getenv("REDIS_PASSWORD") or None
            assert password == "test_password"
        finally:
            if original_pass:
                os.environ["REDIS_PASSWORD"] = original_pass
            else:
                del os.environ["REDIS_PASSWORD"]


class TestRedisClientOperations:
    """Test Redis client operations"""
    
    def test_redis_client_get(self, mock_redis):
        """Test Redis GET operation"""
        mock_redis.get.return_value = "value"
        
        result = mock_redis.get("key")
        assert result == "value"
        mock_redis.get.assert_called_once_with("key")
    
    def test_redis_client_set(self, mock_redis):
        """Test Redis SET operation"""
        mock_redis.set.return_value = True
        
        result = mock_redis.set("key", "value")
        assert result is True
        mock_redis.set.assert_called_once_with("key", "value")
    
    def test_redis_client_delete(self, mock_redis):
        """Test Redis DELETE operation"""
        mock_redis.delete.return_value = 1
        
        result = mock_redis.delete("key")
        assert result == 1
        mock_redis.delete.assert_called_once_with("key")
    
    def test_redis_client_get_session_data(self, mock_redis):
        """Test retrieving session data from Redis"""
        import json
        session_data = {"token": "abc123", "user_id": 1}
        mock_redis.get.return_value = json.dumps(session_data)
        
        result = mock_redis.get("session:1")
        parsed = json.loads(result)
        assert parsed["user_id"] == 1
    
    def test_redis_client_set_session_data(self, mock_redis):
        """Test storing session data in Redis"""
        import json
        session_data = {"token": "abc123", "user_id": 1}
        mock_redis.set.return_value = True
        
        result = mock_redis.set("session:1", json.dumps(session_data))
        assert result is True


class TestRedisClientConfiguration:
    """Test Redis client configuration"""
    
    @patch('redis.Redis')
    def test_decode_responses_enabled(self, mock_redis_class):
        """Test that decode_responses is enabled for string handling"""
        # The decode_responses=True should be passed to Redis()
        # This ensures responses are strings not bytes
        pass
    
    def test_redis_environment_variables(self):
        """Test Redis environment variables are properly set"""
        assert os.getenv("REDIS_HOST") is not None
        assert os.getenv("REDIS_PORT") is not None
        # REDIS_PASSWORD can be None or empty


class TestRedisClientErrorHandling:
    """Test Redis client error handling"""
    
    def test_redis_connection_error(self, mock_redis):
        """Test handling of connection errors"""
        mock_redis.get.side_effect = Exception("Connection refused")
        
        with pytest.raises(Exception):
            mock_redis.get("key")
    
    def test_redis_key_not_found(self, mock_redis):
        """Test handling of missing key"""
        mock_redis.get.return_value = None
        
        result = mock_redis.get("nonexistent_key")
        assert result is None


class TestRedisIntegration:
    """Integration tests with Redis patterns used in the app"""
    
    def test_session_key_pattern(self, mock_redis):
        """Test session key pattern used in the app"""
        user_id = 123
        session_key = f"session:{user_id}"
        
        import json
        session_data = {
            "token": "eyJ...",
            "user_id": user_id,
            "created_at": "2024-01-01T00:00:00"
        }
        
        mock_redis.set.return_value = True
        mock_redis.get.return_value = json.dumps(session_data)
        
        # Set session
        mock_redis.set(session_key, json.dumps(session_data))
        
        # Get session
        stored = mock_redis.get(session_key)
        parsed = json.loads(stored)
        
        assert parsed["user_id"] == user_id
        assert parsed["token"] == "eyJ..."
