# Test Development Guidelines

This document provides guidelines for writing and maintaining tests in the Customer Service project.

## General Principles

### 1. **Test Naming Convention**
```python
# ✅ Good: Clear, describes what is tested
def test_customer_no_field_must_be_required():
def test_schema_rejects_customer_no_exceeding_max_length():
def test_create_customer_endpoint_returns_201():

# ❌ Bad: Vague, unclear intent
def test_customer():
def test_create():
def test_endpoint():
```

### 2. **Test Structure (AAA Pattern)**
```python
def test_example(client, headers_with_token, sample_customer_data):
    # ARRANGE: Set up test data
    test_data = {"customer_no": "CUST001", "name": "Test"}
    
    # ACT: Perform the action being tested
    response = client.post(
        '/create_customer',
        json=test_data,
        headers=headers_with_token
    )
    
    # ASSERT: Verify the results
    assert response.status_code == 201
    assert response.json["customer_no"] == "CUST001"
```

### 3. **One Test = One Concept**
```python
# ✅ Good: Each test focuses on one thing
def test_customer_no_is_required():
    with pytest.raises(ValidationError):
        schema.load({})  # Missing customer_no

def test_customer_no_max_length_is_10():
    with pytest.raises(ValidationError):
        schema.load({"customer_no": "A" * 11})

# ❌ Bad: Test covers multiple concepts
def test_customer_validation():
    # Tests 10 different validation rules at once
    pass
```

### 4. **Prefer Fixtures Over Setup Methods**
```python
# ✅ Good: Use fixtures from conftest.py
def test_example(client, sample_customer_data, headers_with_token):
    response = client.post('/create_customer', json=sample_customer_data)

# ❌ Bad: Duplicate setup code
def test_example():
    client = app.test_client()
    token = create_access_token(identity=1)
    # ... repeat for every test
```

## Test Categories

### Model Tests
Test SQLAlchemy model structure, not behavior.

```python
class TestCustomerModel:
    """Test CustomerModel structure and configuration"""
    
    def test_has_correct_table_name(self):
        assert CustomerModel.__tablename__ == "customers"
    
    def test_customer_id_is_primary_key(self):
        mapper = inspect(CustomerModel)
        pk_columns = [c.key for c in mapper.primary_key]
        assert "customer_id" in pk_columns
```

### Schema Tests
Test Marshmallow validation rules, field requirements, and serialization.

```python
class TestCustomerSchema:
    """Test schema validation"""
    
    def test_customer_no_is_required(self):
        with pytest.raises(ValidationError):
            schema.load({})
    
    def test_name_accepts_none(self):
        result = schema.load({"customer_no": "CUST001", "name": None})
        assert result["name"] is None
    
    def test_share_retailer_values_defaults_to_1(self):
        result = schema.load({"customer_no": "CUST001"})
        assert result["share_retailer_values"] == 1
```

### Resource/Endpoint Tests
Test Flask API endpoints with mocked dependencies.

```python
class TestCreateCustomerEndpoint:
    """Test POST /create_customer"""
    
    @patch('src.customer_service.resources.customer.db')
    def test_creates_customer_successfully(self, mock_db, client, headers_with_token):
        mock_db.session.commit = MagicMock()
        
        response = client.post(
            '/create_customer',
            json={"customer_no": "CUST001"},
            headers=headers_with_token
        )
        
        assert response.status_code == 201
```

### Extension Tests
Test initialization and configuration of external services.

```python
class TestRedisClient:
    """Test Redis client setup"""
    
    def test_redis_client_uses_correct_host(self):
        assert os.getenv("REDIS_HOST") == "localhost"
    
    def test_redis_client_supports_set_get_operations(self, mock_redis):
        mock_redis.set("key", "value")
        mock_redis.get.return_value = "value"
        result = mock_redis.get("key")
        assert result == "value"
```

### App Factory Tests
Test Flask app configuration and initialization.

```python
class TestAppFactory:
    """Test create_app factory"""
    
    def test_app_has_required_config(self, app_with_context):
        assert "API_TITLE" in app_with_context.config
        assert "SQLALCHEMY_DATABASE_URI" in app_with_context.config
    
    def test_cors_is_configured(self, app_with_context):
        assert app_with_context.config["CORS_AUTOMATIC_OPTIONS"] is True
```

## Using Mocks and Patches

### Mock External Dependencies
```python
# ✅ Good: Mock external services
@patch('src.customer_service.resources.customer.db')
def test_customer_creation(mock_db, client):
    mock_db.session.commit = MagicMock()
    response = client.post('/create_customer', json={...})

# ❌ Bad: Trying to call real database
def test_customer_creation(client):
    # This will fail if DB is not available
    response = client.post('/create_customer', json={...})
```

### Use Fixtures for Setup
```python
# ✅ Good: Use provided fixtures
@pytest.fixture
def mock_redis():
    with patch('redis.Redis') as mock:
        yield mock

def test_example(mock_redis):
    mock_redis.get.return_value = "value"

# ❌ Bad: Create mocks inside test
def test_example():
    with patch('redis.Redis') as mock:
        # Harder to reuse, less clean
        pass
```

## Testing Patterns

### Testing Success Cases
```python
def test_create_customer_with_valid_data(client, headers_with_token, sample_customer_data):
    response = client.post(
        '/create_customer',
        json=sample_customer_data,
        headers=headers_with_token
    )
    assert response.status_code == 201
    assert "customer_id" in response.json
```

### Testing Validation Failures
```python
def test_schema_rejects_missing_customer_no():
    schema = CustomerSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load({"name": "Test"})
    assert "customer_no" in exc_info.value.messages
```

### Testing Error Handling
```python
def test_endpoint_handles_database_error(client, headers_with_token):
    with patch('src.customer_service.resources.customer.db') as mock_db:
        mock_db.session.commit.side_effect = SQLAlchemyError("DB Error")
        mock_db.session.rollback = MagicMock()
        
        response = client.post(
            '/create_customer',
            json={"customer_no": "CUST001"},
            headers=headers_with_token
        )
        assert response.status_code == 500
```

### Testing Authentication
```python
def test_endpoint_requires_token(client):
    """Test that endpoint rejects requests without token"""
    response = client.post('/create_customer', json={...})
    assert response.status_code in [401, 422]

def test_endpoint_rejects_expired_token(client, expired_token):
    """Test that expired tokens are rejected"""
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.post('/create_customer', json={...}, headers=headers)
    assert response.status_code == 401
```

## Code Coverage

### Coverage Goals
- **Target**: 85%+ for all src/ modules
- **Exceptions**: External API calls, rarely-used branches

### Checking Coverage
```bash
# Terminal report showing missing lines
pytest --cov=src --cov-report=term-missing

# HTML report for detailed analysis
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

### Improving Coverage

**Find untested code:**
```bash
pytest --cov=src --cov-report=term-missing | grep -E "^\s+[0-9]+"
```

**Add tests for missing lines:**
```python
# If test shows line 42 is not covered, write a test for that code path
def test_missing_code_path():
    # Test the specific scenario that exercises line 42
    pass
```

## Common Testing Mistakes

### ❌ Mistake: Hardcoded values in tests
```python
def test_bad(client):
    response = client.post('/customer/123', json={...})
    # If customer ID changes, test breaks
```

**✅ Solution: Use fixtures or parametrize**
```python
def test_good(client, sample_customer_data):
    response = client.post('/create_customer', json=sample_customer_data)
    # Uses fixture data, more flexible
```

### ❌ Mistake: Testing multiple concepts in one test
```python
def test_bad(schema):
    # Tests required fields, length validation, and defaults all at once
    # If one fails, hard to debug
    pass
```

**✅ Solution: Separate tests**
```python
def test_customer_no_required(schema):
    with pytest.raises(ValidationError):
        schema.load({})

def test_customer_no_max_length(schema):
    with pytest.raises(ValidationError):
        schema.load({"customer_no": "A" * 11})

def test_share_retailer_values_default(schema):
    result = schema.load({"customer_no": "CUST001"})
    assert result["share_retailer_values"] == 1
```

### ❌ Mistake: Not using mocks for external services
```python
def test_bad(client):
    # This test depends on actual database being up
    response = client.post('/create_customer', json={...})
```

**✅ Solution: Mock external dependencies**
```python
@patch('src.customer_service.resources.customer.db')
def test_good(mock_db, client):
    mock_db.session.commit = MagicMock()
    response = client.post('/create_customer', json={...})
    # Test runs without needing real database
```

## Performance Tips

1. **Use mocks instead of real services** - Tests run 100x faster
2. **Parametrize tests** - Test multiple cases with one test function
3. **Use fixtures** - Setup is done once, reused across tests
4. **Avoid sleeps** - Use mocks instead of `time.sleep()`

```python
# ✅ Good: Parametrized test (one function, multiple cases)
@pytest.mark.parametrize("value,expected", [
    (0, "disabled"),
    (1, "enabled"),
])
def test_flag_values(value, expected):
    result = process_flag(value)
    assert result == expected

# ❌ Bad: Duplicate tests
def test_flag_value_0():
    assert process_flag(0) == "disabled"

def test_flag_value_1():
    assert process_flag(1) == "enabled"
```

## Adding New Tests

When implementing a new feature:

1. **Create test file** in appropriate directory
2. **Write test class** with descriptive name
3. **Use fixtures** from conftest.py
4. **Follow AAA pattern** (Arrange, Act, Assert)
5. **Test success AND failure** cases
6. **Check coverage** with `pytest --cov`

Example: Testing a new endpoint

```python
# tests/unit/resources/test_new_endpoint.py
import pytest

class TestNewFeatureEndpoint:
    """Test GET /new_feature endpoint"""
    
    def test_endpoint_returns_data(self, client, headers_with_token):
        response = client.get('/new_feature', headers=headers_with_token)
        assert response.status_code == 200
        assert "data" in response.json
    
    def test_endpoint_requires_authentication(self, client):
        response = client.get('/new_feature')
        assert response.status_code == 401
    
    def test_endpoint_returns_404_when_not_found(self, client, headers_with_token):
        response = client.get('/new_feature/999', headers=headers_with_token)
        assert response.status_code == 404
```

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Flask Testing Guide](https://flask.palletsprojects.com/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/testing/)
- [Unittest Mock](https://docs.python.org/3/library/unittest.mock.html)
- [Coverage.py](https://coverage.readthedocs.io/)
