# Development Setup

## Virtual Environment

```
$ uv init --python 3.12
$ . ./set_env.sh
$ uv sync


$ uv add --group prod gunicorn mysqlclient
```

## Django Project Setup

```
$ uv run django-admin startproject accounts app
$ cd app

$ uv run manage.py migrate
$ uv run manage.py createsuperuser
$ uv run manage.py startapp main

```
