.PHONY: help install test test-cov test-watch test-verbose test-failed clean coverage-report coverage-html lint format

help:
	@echo "Customer Service Test Commands"
	@echo "=============================="
	@echo ""
	@echo "Setup:"
	@echo "  make install           Install dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test              Run all unit tests"
	@echo "  make test-verbose      Run tests with verbose output"
	@echo "  make test-cov          Run tests with coverage report"
	@echo "  make test-watch        Run tests and watch for changes"
	@echo "  make test-failed       Re-run only failed tests"
	@echo "  make test-unit         Run only unit tests"
	@echo ""
	@echo "Coverage:"
	@echo "  make coverage-report   Generate coverage report (terminal)"
	@echo "  make coverage-html     Generate HTML coverage report"
	@echo "  make coverage-xml      Generate XML coverage report (CI)"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint              Run linters (pylint, flake8)"
	@echo "  make format            Format code (black)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean             Remove test artifacts and cache"

install:
	pip install -r requirements.txt

test:
	pytest

test-verbose:
	pytest -v

test-cov:
	pytest --cov=src --cov-report=term-missing

test-watch:
	pytest-watch

test-failed:
	pytest --lf

test-unit:
	pytest tests/unit/

coverage-report:
	pytest --cov=src --cov-report=term-missing --cov-fail-under=85

coverage-html:
	pytest --cov=src --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

coverage-xml:
	pytest --cov=src --cov-report=xml --cov-report=term-missing --cov-fail-under=85
	@echo "Coverage report generated in coverage.xml"

lint:
	pylint src/ tests/ --fail-under=8.0 || true
	flake8 src/ tests/ --max-line-length=120 || true

format:
	black src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .tox -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name .coverage -delete
	find . -type f -name coverage.xml -delete
	find . -type f -name "*.pyc" -delete
	@echo "Cleaned up test artifacts"

.DEFAULT_GOAL := help
