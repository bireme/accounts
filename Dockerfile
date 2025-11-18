############################################
# BASE STAGE – shared environment
############################################
FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV="/.venv" \
    PATH="/.venv/bin:$PATH"

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


############################################
# BUILDER STAGE – compile dependencies
############################################
FROM base AS builder

# Install build deps (only for building mysqlclient)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

# Build dependencies into /.venv
RUN uv sync --frozen --no-install-project --active

# Ensure correct ownership
RUN chown -R appuser:appuser /.venv


############################################
# DEVELOPMENT STAGE
############################################
FROM base AS dev

# Install minimal runtime MySQL client
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy built virtualenv
COPY --from=builder /.venv /.venv

# Fix permissions
RUN chown -R appuser:appuser /app /.venv

# Switch to non-root user
USER appuser

EXPOSE 8000

WORKDIR /app/app

CMD ["uv", "run", "--active", "manage.py", "runserver", "0.0.0.0:8000"]


############################################
# PRODUCTION STAGE
############################################
FROM base AS prod

# Install runtime MySQL client only
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy built virtualenv
COPY --from=builder /.venv /.venv

# Copy application code
COPY ./app /app/

# Django static folder
RUN mkdir -p /app/static_files

# Fix permissions
RUN chown -R appuser:appuser /app /.venv

# Run as non-root user
USER appuser

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "accounts.wsgi:application"]
