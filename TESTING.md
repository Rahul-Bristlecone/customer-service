# Testing Guide

This project uses:
- pytest
- pytest-cov
- HTML coverage report

## Install

```bash
python -m pip install -r requirements.txt
```

## Run tests

```bash
python -m pytest
```

Run only unit tests:

```bash
python -m pytest tests/unit/
```

Re-run failed tests:

```bash
python -m pytest --lf
```

## Coverage

Terminal report:

```bash
python -m pytest --cov=src --cov-report=term-missing
```

HTML report:

```bash
python -m pytest --cov=src --cov-report=html --cov-report=term-missing
```

Open report on Windows:

```bash
start htmlcov/index.html
```

Generate XML report (for CI):

```bash
python -m pytest --cov=src --cov-report=xml --cov-report=term-missing
```

## Optional: same commands via Makefile

```bash
make test
make test-cov
make coverage-html
make coverage-xml
```

## Notes

- Test files are under `tests/unit/`
- Shared fixtures are in `tests/conftest.py`
- Pytest settings are in `pytest.ini`
