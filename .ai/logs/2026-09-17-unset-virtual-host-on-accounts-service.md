# 2026-09-17 — Unset VIRTUAL_HOST on the `accounts` service

## Problem

`docker-compose.yml` loads `.env` into the `accounts` container via `env_file`.
Since `.env` also contains `VIRTUAL_HOST` (needed for `${VIRTUAL_HOST}`
interpolation on the `webserver` service), the `accounts` container ended up
with the same `VIRTUAL_HOST` as `accounts-webserver`. nginx-proxy then
load-balanced requests between gunicorn (`accounts:8000`) and nginx
(`accounts-webserver:80`), bypassing the nginx `/static/` location and causing
intermittent static-file 404s in production.

## Why not just remove `env_file`

`env_file` is the only source of the Django runtime configuration read in
`src/accounts/settings.py` (`APP_SECRET_KEY`, `APP_ALLOWED_HOSTS`,
`CSRF_TRUSTED_ORIGINS`, `DATABASE_*`, `EMAIL_*`, `LOG_LEVEL`). Removing it would
make the app fall back to the insecure default secret key, `localhost`-only
allowed hosts (400 on every request), SQLite and a local SMTP server.

Compose reads `.env` for `${...}` interpolation independently of `env_file`, so
the `webserver` values would keep working — but the app would break.

## Change

`docker-compose.yml` — `accounts` service now keeps `env_file: .env` and adds:

```yaml
    environment:
      # override values from .env: only the webserver must be routed by nginx-proxy
      - VIRTUAL_HOST=
      - LETSENCRYPT_HOST=
```

`environment` takes precedence over `env_file`, so the container sees empty
values and nginx-proxy/acme-companion ignore it. The `webserver` service is
unchanged and remains the only routed container.

## Verification

`docker compose config` shows `VIRTUAL_HOST: ""` and `LETSENCRYPT_HOST: ""` on
`accounts`, and `VIRTUAL_HOST: <host>` on `webserver`. All other `.env` values
are still injected into `accounts`.

## Deploy

```
make down && make start
```
