# *********** Stage 1: Builder stage ************
# Purpose: Build and install Python dependencies in an isolated environment
FROM python:3.12-slim AS builder

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src/ ./src

RUN pip install --upgrade pip setuptools wheel && \
    pip wheel --no-build-isolation --wheel-dir=/app/wheels .

# *********** Stage 2: Final stage - Runtime environment ************
# Purpose: Create a minimal, secure runtime image with only necessary artifacts
FROM python:3.12-slim

WORKDIR /app

# Create a dedicated non-root user for running the application
# Running as non-root improves container security by limiting privileges
RUN groupadd -r usergroup && useradd -r -g usergroup user

COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/* \
    && rm -rf /wheels

ENV PYTHONPATH=/src

COPY run.py ./

# Switch to non-root user for all subsequent operations
USER user

# Expose application port (5000) for external access
EXPOSE 5000

# Define a health check to monitor container availability
# - Runs every 30s, times out after 10s
# - Retries 3 times before marking container unhealthy
# - Uses Python socket to verify the app is listening on port 5000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import socket; s=socket.socket(); s.connect(('localhost',5000))"

# Default command: start the application
# Using explicit Python invocation ensures consistent entrypoint behavior
CMD ["python", "run.py"]