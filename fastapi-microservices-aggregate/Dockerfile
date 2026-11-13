FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast, reliable dependency installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy project definition and install production dependencies
COPY pyproject.toml .
RUN uv pip install --system --no-cache "."

# Copy application source code
COPY shared/ ./shared/
COPY services/ ./services/
COPY infra/ ./infra/

# Default port and healthcheck
EXPOSE 8000 8001 8002 8003 8004

CMD ["uvicorn", "services.gateway_aggregator.main:app", "--host", "0.0.0.0", "--port", "8000"]
