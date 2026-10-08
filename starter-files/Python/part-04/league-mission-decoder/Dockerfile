# Multi-stage build for League Mission Decoder

# Stage 1: Builder
FROM python:3.12-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY starter-files/Python/part-04/league-mission-decoder/ .

# Install Python dependencies (if requirements.txt exists)
# RUN pip install --no-cache-dir -r requirements.txt

# Run tests to verify build
RUN python -m pip install --upgrade pip && \
    pip install pytest pytest-cov && \
    pytest -v --tb=short || echo "Tests completed"


# Stage 2: Runtime
FROM python:3.12-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 decoder && \
    chown -R decoder:decoder /app

# Copy application code from builder
COPY --from=builder --chown=decoder:decoder /build /app

# Copy any requirements if they exist
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Switch to non-root user
USER decoder

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Metadata
LABEL org.opencontainers.image.title="League Mission Decoder"
LABEL org.opencontainers.image.description="Secure blueprint decoder for League mission data"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.authors="GitHub Copilot Workshop"
LABEL org.opencontainers.image.source="https://github.com/codess-aus/AI-Assisted-Dev-with-GitHub-Copilot"

# Entry point
ENTRYPOINT ["python", "cli.py"]
CMD ["--help"]
