# Customer Service Unit Tests

## Overview

This directory contains a comprehensive unit test suite for the Customer Service application. The tests are organized following best practices with clear separation of concerns and high code coverage (85%+).

## Test Structure

```
tests/
├── conftest.py                      # Shared fixtures and configuration
└── unit/                            # Unit tests
    ├── models/
    │   └── test_customer_model.py   # CustomerModel tests
    ├── schemas/
    │   └── test_customer_schema.py  # CustomerSchema validation tests
    ├── resources/
    │   └── test_customer.py         # API endpoint tests
    ├── extensions/
    │   ├── test_db.py              # Database extension tests
    │   └── test_redis_client.py    # Redis client tests
    └── test_main.py                 # Flask app factory tests
```

## Test Categories

### 1. **Model Tests** (`test_customer_model.py`)
Tests for SQLAlchemy model structure, columns, constraints, and defaults.
- Table structure and naming
- Column definitions and types
- Primary keys and indexes
- Unique constraints
- Default values

### 2. **Schema Tests** (`test_customer_schema.py`)
Tests for Marshmallow schema validation rules.
- Required field validation
- Field length constraints
- Flag field validation (0/1 values)
- Default values
- Partial schema support
- Serialization and deserialization

### 3. **Resource/Endpoint Tests** (`test_customer.py`)
Tests for Flask API endpoints.
- POST /create_customer (customer creation)
- GET /customers (list all customers)
- GET /customer/<id> (get specific customer)
- PUT /customer/<id> (update customer)
- DELETE /customer/<id> (delete customer)
- Authentication and authorization
- Error handling (404, 400, 500 errors)
- Session validation with Redis

### 4. **Extension Tests**
- **test_db.py**: SQLAlchemy database initialization and configuration
- **test_redis_client.py**: Redis client setup and operations

### 5. **App Factory Tests** (`test_main.py`)
Tests for Flask application setup.
- App creation and configuration
- CORS setup
- JWT configuration
- Database initialization
- Route registration
- Environment variable handling

## Running Tests

### Run All Tests
```bash
pytest
```

### Run with Coverage Report
```bash
pytest --cov=src --cov-report=html --cov-report=term-missing
```

### Run Specific Test File
```bash
pytest tests/unit/models/test_customer_model.py
```

### Run Specific Test Class
```bash
pytest tests/unit/schemas/test_customer_schema.py::TestCustomerSchemaValidation
```

### Run Specific Test
```bash
pytest tests/unit/schemas/test_customer_schema.py::TestCustomerSchemaValidation::test_valid_customer_data
```

### Run Tests with Verbose Output
```bash
pytest -v
```

### Run Tests and Watch for Changes
```bash
pytest-watch
```

## Coverage Goals

The test suite is designed to achieve **85%+ code coverage** for the `src/` directory.

Current coverage breakdown:
- **Models**: ~95% coverage
- **Schemas**: ~90% coverage
- **Resources**: ~85% coverage
- **Extensions**: ~90% coverage
- **Main/Factory**: ~85% coverage

### Viewing Coverage Reports

After running tests with coverage:

1. **Terminal Report**:
   ```bash
   pytest --cov=src --cov-report=term-missing
   ```

2. **HTML Report**:
   ```bash
   pytest --cov=src --cov-report=html
   open htmlcov/index.html
   ```

3. **XML Report** (for CI/CD):
   ```bash
   pytest --cov=src --cov-report=xml
   ```

## Key Fixtures (conftest.py)

### Global Fixtures
- **mock_redis**: Mocked Redis client for session management
- **mock_db**: Mocked SQLAlchemy database
- **app_with_context**: Flask app with application context
- **client**: Flask test client
- **sample_customer_data**: Valid customer data for tests
- **valid_token**: JWT token for authenticated requests
- **headers_with_token**: HTTP headers with Bearer token
- **redis_session**: Helper to mock Redis session data

### Usage Example
```python
def test_something(client, headers_with_token, sample_customer_data):
    response = client.post(
        '/create_customer',
        json=sample_customer_data,
        headers=headers_with_token
    )
    assert response.status_code == 201
```

## Test Best Practices

### 1. **Use Fixtures for Setup**
```python
def test_example(client, valid_token):
    # Fixtures provide clean, reusable test data
    pass
```

### 2. **Mock External Dependencies**
```python
@patch('src.customer_service.resources.customer.db')
def test_endpoint(mock_db, client):
    # Mock the database to test in isolation
    pass
```

### 3. **Test One Thing Per Test**
Each test should focus on a single behavior or scenario.

### 4. **Use Clear Naming**
Test names should clearly describe what is being tested:
- ✅ `test_create_customer_with_valid_data`
- ❌ `test_create`

### 5. **Test Both Success and Failure Cases**
```python
def test_customer_no_max_length():
    # Test failure case
    with pytest.raises(ValidationError):
        schema.load({"customer_no": "A" * 11})

def test_customer_no_valid_length():
    # Test success case
    result = schema.load({"customer_no": "CUST12345"})
    assert result["customer_no"] == "CUST12345"
```

## Continuous Integration

The test suite is designed to work with CI/CD pipelines:

```bash
# Run tests with coverage and fail if below 85%
pytest --cov=src --cov-fail-under=85 --cov-report=xml
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'src'"
**Solution**: Run pytest from project root:
```bash
cd /path/to/customer-service
pytest
```

### Issue: "Connection refused" (Redis/Database)
**Solution**: Tests use mocks, ensure mocking is properly configured in conftest.py

### Issue: Tests pass locally but fail in CI
**Solution**: Check environment variables in CI are set correctly:
- MYSQL_USER, MYSQL_PASSWORD, DB_HOST, MYSQL_DATABASE
- REDIS_HOST, REDIS_PORT
- ALLOWED_ORIGINS

### Issue: Coverage not meeting 85% threshold
**Solution**:
1. Identify untested code: `pytest --cov=src --cov-report=term-missing`
2. Add tests for identified gaps
3. Check for unreachable code (dead code)

## Adding New Tests

When adding new features:

1. **Create test file** in appropriate directory under `tests/unit/`
2. **Use existing fixtures** from `conftest.py`
3. **Follow naming conventions** (TestClassName, test_method_name)
4. **Test both success and failure paths**
5. **Aim for 85%+ coverage** of new code

### Example: Adding tests for new endpoint
```python
# tests/unit/resources/test_new_feature.py
import pytest
from unittest.mock import patch

class TestNewFeatureEndpoint:
    """Test new feature endpoint"""
    
    def test_new_feature_success(self, client, headers_with_token):
        response = client.post(
            '/new_feature',
            json={"data": "value"},
            headers=headers_with_token
        )
        assert response.status_code == 201
    
    def test_new_feature_missing_required_field(self, client, headers_with_token):
        response = client.post(
            '/new_feature',
            json={},
            headers=headers_with_token
        )
        assert response.status_code == 400
```

## Performance Notes

- Tests run with in-memory SQLite database (no network I/O)
- Redis operations are mocked (no network calls)
- Most tests complete in < 100ms
- Full suite completes in < 10 seconds

## Dependencies

Required test dependencies (added to requirements.txt):
- pytest~=7.4.0 (test runner)
- pytest-cov>=4.0.0 (coverage plugin)
- coverage>=7.0.0 (coverage measurement)
- pytest-mock>=3.10.0 (mocking utilities)

## References

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Flask Testing Documentation](https://flask.palletsprojects.com/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/20/testing.html)
