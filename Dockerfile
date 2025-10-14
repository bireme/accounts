########### BASE STAGE ###########
FROM python:3.12-alpine AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

EXPOSE 8000

########### DEV STAGE ###########
FROM base AS dev

# Install dependencies
COPY pyproject.toml uv.lock .
RUN uv sync

# Set app directory
WORKDIR app/


########### PRODUCTION STAGE ###########
FROM base AS prod

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    mariadb-dev \
    python3-dev

# Install dependencies
COPY pyproject.toml uv.lock .
RUN uv sync --group prod

# Set app directory
WORKDIR app/

# create directory for collectstatic command
RUN mkdir /app/static_files

# Copy src files
COPY ./app /app/

# Execute app
CMD uv run gunicorn --bind 0.0.0.0:8000 accounts.wsgi
