# Customer Service API

[![Unit Tests & Coverage](https://github.com/yourusername/customer-service/actions/workflows/tests.yml/badge.svg)](https://github.com/yourusername/customer-service/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/yourusername/customer-service/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/customer-service)

A comprehensive Flask-based REST API for managing customer data with JWT authentication, Redis session management, and MySQL database persistence.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [Development](#development)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

✨ **Core Features:**
- RESTful API endpoints for CRUD operations on customer records
- JWT-based authentication and authorization
- Redis session management for active session tracking
- MySQL database for persistent data storage
- Comprehensive validation using Marshmallow schemas
- CORS support for cross-origin requests
- Automatic API documentation with Swagger UI
- Extensive business configuration flags and EDI settings

📊 **Customer Configuration Includes:**
- General customer information (name, ABN, reference codes)
- Order management flags (changes, back orders, shipments)
- Validation rules (retailer, trade units, pack sizes, pallets)
- Picking preferences (hand-pick, over-pick, auto-create ratios)
- EDI/EDX configuration (address, message format, line terminators)
- Pricing rules and tax handling
- Label and shipment configuration
- RPO (Replenishment Purchase Order) settings

## Tech Stack

- **Framework**: Flask 3.0.3
- **API**: Flask-RESTful with flask-smorest
- **Database**: SQLAlchemy ORM, MySQL
- **Authentication**: Flask-JWT-Extended
- **Validation**: Marshmallow
- **Caching**: Redis
- **CORS**: Flask-CORS
- **Python**: 3.10, 3.11
- **Testing**: pytest with 85%+ coverage
- **Deployment**: Docker, Kubernetes-ready

## Prerequisites

- Python 3.10 or 3.11
- MySQL 8.0+
- Redis 7.0+
- Docker & Docker Compose (optional)
- pip or poetry for dependency management

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/customer-service.git
cd customer-service
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=true

# Database Configuration
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
MYSQL_DATABASE=customer_service

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

## Configuration

### Database Setup

```bash
# Create MySQL database
mysql -u root -p -e "CREATE DATABASE customer_service;"

# Apply migrations (if using Alembic)
alembic upgrade head
```

### Redis Setup

Make sure Redis is running:

```bash
# Using Docker
docker run -d -p 6379:6379 redis:7-alpine

# Or using local Redis
redis-server
```

## Running the Application

### Local Development

```bash
# Run with Flask development server
python run.py

# Or using flask CLI
flask run

# Run with auto-reload
flask run --reload
```

The API will be available at `http://localhost:5000`

Swagger documentation: `http://localhost:5000/swagger-ui`

### Using Gunicorn (Production-like)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## API Documentation

### Base URL

```
http://localhost:5000
```

### Endpoints

#### Create Customer

```http
POST /create_customer
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "customer_no": "CUST001",
  "name": "Acme Corp",
  "abn": "12345678901234",
  "allow_change_order": 1,
  "allow_back_order": 1
}

Response: 201 Created
```

#### Get All Customers

```http
GET /customers
Authorization: Bearer <JWT_TOKEN>

Response: 200 OK
[
  {
    "customer_id": 1,
    "customer_no": "CUST001",
    "name": "Acme Corp",
    ...
  }
]
```

#### Get Specific Customer

```http
GET /customer/{customer_id}
Authorization: Bearer <JWT_TOKEN>

Response: 200 OK
{
  "customer_id": 1,
  "customer_no": "CUST001",
  "name": "Acme Corp",
  ...
}
```

#### Update Customer

```http
PUT /customer/{customer_id}
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "name": "Acme Corporation",
  "allow_change_order": 0
}

Response: 200 OK
```

#### Delete Customer

```http
DELETE /customer/{customer_id}
Authorization: Bearer <JWT_TOKEN>

Response: 200 OK
{
  "message": "Customer deleted successfully"
}
```

### Authentication

All endpoints (except login) require JWT authentication. Include the token in the Authorization header:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Full API Documentation

Swagger UI is available at: `http://localhost:5000/swagger-ui`

## Testing

## ✨ Key Features

✅ Comprehensive fixtures for reusable setup
✅ Mocked external dependencies (DB, Redis)
✅ Clear test naming and organization
✅ Both success and failure test cases
✅ Authentication/authorization testing
✅ Error handling coverage
✅ Full documentation and examples
✅ CI/CD pipeline ready
✅ Easy to extend and maintain

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
# Terminal report
pytest --cov=src --cov-report=term-missing

# HTML report
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

### Using Makefile Commands

```bash
make test              # Run all tests
make test-cov          # With coverage
make coverage-html     # HTML coverage report
make test-verbose      # Verbose output
make lint              # Run linters
make format            # Format code
make clean             # Clean artifacts
```

### Test Coverage

- **Target**: 85%+
- **Achieved**: ~90%
- **Test Files**: 6 (125+ test cases)

For detailed testing information, see [TESTING.md](TESTING.md)

## Docker Deployment

### Build Docker Image

```bash
docker build -t customer-service:latest .
```

### Run with Docker Compose

```bash
docker-compose up -d
```

This will start:
- Customer Service API (port 5000)
- MySQL Database (port 3306)
- Redis Cache (port 6379)

### Docker Compose Override

Create `docker-compose.override.yml` for local development:

```yaml
version: '3.8'
services:
  customer-service:
    build: .
    volumes:
      - .:/app
    environment:
      FLASK_DEBUG: "true"
```

## Development

### Code Style

This project uses:
- **Black** for code formatting
- **pylint** for linting
- **flake8** for style checking

### Format Code

```bash
black src/ tests/
```

### Run Linters

```bash
flake8 src/ tests/
pylint src/
```

### Type Checking

```bash
mypy src/
```

### Pre-commit Hooks

Set up pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

## Project Structure

```
customer-service/
├── src/
│   └── customer_service/
│       ├── main.py                    # Flask app factory
│       ├── models/
│       │   └── customer_model.py      # SQLAlchemy models
│       ├── schemas/
│       │   └── customer_schema.py     # Marshmallow schemas
│       ├── resources/
│       │   └── customer.py            # API endpoints
│       └── extentions/
│           ├── db.py                  # Database setup
│           └── redis_client.py        # Redis client
├── tests/
│   ├── conftest.py                    # Pytest fixtures
│   └── unit/                          # Unit tests
│       ├── models/
│       ├── schemas/
│       ├── resources/
│       └── extensions/
├── .github/
│   └── workflows/
│       └── tests.yml                  # CI/CD pipeline
├── Dockerfile                         # Docker configuration
├── docker-compose.yml                 # Multi-container setup
├── requirements.txt                   # Python dependencies
├── pytest.ini                         # Pytest configuration
├── Makefile                           # Development commands
├── .gitignore                         # Git ignore rules
├── .dockerignore                      # Docker ignore rules
└── README.md                          # This file
```

## API Testing with cURL

### Create Customer

```bash
curl -X POST http://localhost:5000/create_customer \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"customer_no": "CUST001", "name": "Test Customer"}'
```

### Get Customers

```bash
curl -X GET http://localhost:5000/customers \
  -H "Authorization: Bearer <TOKEN>"
```

## Environment-Specific Configuration

### Development
```env
FLASK_ENV=development
FLASK_DEBUG=true
SQLALCHEMY_ECHO=true
```

### Staging
```env
FLASK_ENV=staging
FLASK_DEBUG=false
LOG_LEVEL=INFO
```

### Production
```env
FLASK_ENV=production
FLASK_DEBUG=false
LOG_LEVEL=WARNING
```

## Troubleshooting

### Database Connection Issues

```bash
# Check MySQL is running
mysql -u user -p -e "SELECT 1"

# Verify database exists
mysql -u user -p -e "SHOW DATABASES"
```

### Redis Connection Issues

```bash
# Test Redis connection
redis-cli ping

# Check Redis is running
redis-cli info server
```

### JWT Token Issues

```bash
# Generate test token
python
>>> from flask_jwt_extended import create_access_token
>>> token = create_access_token(identity=1)
>>> print(token)
```

### Port Already in Use

```bash
# Change Flask port
flask run --port 5001

# Or using environment variable
export FLASK_ENV=development
export FLASK_RUN_PORT=5001
flask run
```

## Performance Considerations

- **Database Indexing**: user_id and customer_no are indexed for fast lookups
- **Redis Caching**: Session data is cached in Redis for quick validation
- **Connection Pooling**: SQLAlchemy handles connection pooling automatically
- **Async Support**: Can be extended with Celery for background tasks

## Security

- **JWT Tokens**: Use strong secret key in production
- **CORS**: Configure allowed origins carefully
- **Database**: Use strong passwords, limit user privileges
- **Redis**: Protect with password in production
- **HTTPS**: Use HTTPS in production
- **Input Validation**: All inputs validated through Marshmallow schemas
- **SQL Injection**: Protected by SQLAlchemy ORM

## Monitoring & Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Customer created", extra={"customer_id": 1})
logger.error("Database error", exc_info=True)
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Write tests for new features
5. Ensure tests pass (`pytest --cov=src --cov-fail-under=85`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Make changes and test
pytest --cov=src

# 3. Format code
make format

# 4. Commit
git add .
git commit -m "Add my feature"

# 5. Push and create PR
git push origin feature/my-feature
```

## License

This project is licensed under the License Agreement - see [LICENCE](LICENCE) file for details.

## Support

For support, please:
1. Check existing issues on GitHub
2. Create a new issue with detailed description
3. Contact the development team

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

**Version**: 1.0.0  
**Last Updated**: 2026-06-30  
**Status**: Active Development
