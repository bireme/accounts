# BASE STAGE
FROM python:2.7.13-alpine AS base

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONWARNINGS='ignore::DeprecationWarning'

# copy base requirements
COPY ./requirements.txt /app/requirements.txt

# install base dependencies
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    python-dev \
    && apk add --no-cache mariadb-dev \
    && pip install --upgrade pip setuptools && pip install --no-cache-dir -r /app/requirements.txt \
    && apk del .build-deps 

EXPOSE 8000

WORKDIR /app


# TEST STAGE
FROM base AS test

RUN mkdir /app/static_files

# copy aplication files to image
# COPY ./bireme/ /app/
