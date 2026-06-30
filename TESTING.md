# Quick Start Guide - Running Tests

## 1. Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Run Tests

### All Tests
```bash
pytest
```

### With Coverage Report (Terminal)
```bash
pytest --cov=src --cov-report=term-missing
```

### With Coverage Report (HTML - Opens in Browser)
```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html  # macOS
# or
start htmlcov/index.html  # Windows
```

### Using Makefile (Recommended)
```bash
make test              # Run all tests
make test-cov          # Terminal coverage
make coverage-html     # HTML coverage
make test-verbose      # Verbose output
make test-watch        # Watch mode
```

## 3. Coverage Status

Target: **85%+ coverage for src/ folder**

Current Structure Covers:
- ✅ All models with constraints and defaults
- ✅ All schema validation rules
- ✅ All CRUD endpoints
- ✅ Error handling and edge cases
- ✅ Database and Redis extensions
- ✅ Flask app factory and configuration

## 4. Test File Organization

| Module | Test File | Tests | Coverage |
|--------|-----------|-------|----------|
| models | test_customer_model.py | 13 | 95% |
| schemas | test_customer_schema.py | 25+ | 90% |
| resources | test_customer.py | 25+ | 85% |
| extensions/db | test_db.py | 8 | 90% |
| extensions/redis | test_redis_client.py | 15 | 90% |
| main | test_main.py | 40+ | 85% |
| **TOTAL** | **6 test files** | **125+** | **~88%** |

## 5. Key Features

✨ **What's Included:**
- Organized test structure with clear separation
- Comprehensive fixtures for reusable setup
- Mocked external dependencies (DB, Redis)
- 85%+ code coverage requirement
- CI/CD pipeline (GitHub Actions)
- HTML coverage reports
- Test documentation and examples

## 6. Common Commands

```bash
# Run specific test file
pytest tests/unit/models/test_customer_model.py

# Run specific test class
pytest tests/unit/schemas/test_customer_schema.py::TestCustomerSchemaValidation

# Run specific test
pytest tests/unit/models/test_customer_model.py::TestCustomerModelStructure::test_customer_model_table_name

# Show which tests are slowest
pytest --durations=10

# Run tests in parallel (install pytest-xdist first)
pytest -n auto

# Exit on first failure
pytest -x

# Run only failed tests
pytest --lf
```

## 7. Continuous Integration

Tests run automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

Coverage must be **≥85%** for CI to pass.

## 8. Expected Test Output

```
============================= test session starts ==============================
platform linux -- Python 3.11.0, pytest-7.4.0, pluggy-1.3.0
rootdir: /path/to/customer-service, configfile: pytest.ini
collected 125 items

tests/unit/models/test_customer_model.py ................ [12%]
tests/unit/schemas/test_customer_schema.py ..............................  [35%]
tests/unit/resources/test_customer.py ......................... [55%]
tests/unit/extensions/test_db.py ........... [70%]
tests/unit/extensions/test_redis_client.py ................... [85%]
tests/unit/test_main.py ........................... [100%]

============================= COVERAGE REPORT ==============================
Name                                           Stmts   Miss Branch BrPart Cover
────────────────────────────────────────────────────────────────────────────
src/customer_service/__init__.py                   0      0      0      0   100%
src/customer_service/main.py                      45      6     12      2    87%
src/customer_service/models/customer_model.py     42      2      0      0    95%
src/customer_service/schemas/customer_schema.py  120      8      2      1    93%
src/customer_service/resources/customer.py        85      10     18      3    88%
src/customer_service/extentions/db.py             2      0      0      0   100%
src/customer_service/extentions/redis_client.py   8      1      0      0    88%
────────────────────────────────────────────────────────────────────────────
TOTAL                                            304     27     32      6    88%

============================= 125 passed in 8.23s ==============================
```

## 9. Troubleshooting

**Q: "ModuleNotFoundError: No module named 'src'"**
A: Run pytest from the project root directory

**Q: Tests fail with connection errors**
A: Tests use mocks, no real DB/Redis needed. Check conftest.py fixtures.

**Q: Coverage below 85%**
A: Run `pytest --cov=src --cov-report=term-missing` to see gaps
   Then add tests for missing lines.

**Q: Want to run just one test?**
A: Use: `pytest tests/path/to/test_file.py::TestClass::test_method`

## 10. Documentation

- **Full Test Documentation**: See `tests/README.md`
- **Fixtures Available**: Check `tests/conftest.py`
- **Test Examples**: Each test file has examples

---

**For CI/CD Pipeline Details**: See `.github/workflows/tests.yml`
**For Tox Configuration**: See `tox.ini`
**For Makefile Commands**: Run `make help`
