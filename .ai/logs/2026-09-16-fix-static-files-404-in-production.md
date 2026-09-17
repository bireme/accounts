# Fix static files 404 in production

## Problem

Production logs showed Django returning 404 for static assets referenced by
`src/templates/base.html`:

```
WARNING django.request: Not Found: /static/css/screen.css
WARNING django.request: Not Found: /static/bootstrap/js/bootstrap-typeahead.js
WARNING django.request: Not Found: /static/bootstrap/js/bootstrap-modal.js
```

The files exist in `src/static/`. The 404s were logged by **Django** (not
nginx), meaning `/static/` requests reached gunicorn instead of being served
by the `location /static/` alias in `conf/nginx/`. With `APP_DEBUG=0` Django
does not serve static files. Additionally, nothing in the deploy populated the
`static_files` volume — `make collectstatic` had to be run by hand after every
deploy.

Decision: static files must be served by nginx (WhiteNoise was tried and
removed at the user's request).

## Changes

- `Dockerfile` (prod stage): replaced `mkdir -p /app/static_files` with a
  build-time `manage.py collectstatic --noinput`, so the image ships with
  `/app/static_files` already populated and seeds the `static_files` volume
  shared with the `accounts-webserver` nginx container.

## Verification

- `make build` → `bireme/accounts:1.0.65`; `static_files/css/screen.css` and
  `static_files/bootstrap/js/bootstrap-{modal,typeahead}.js` are present in
  the image.

## Deploy notes

- The existing `static_files` named volume in production will **not** be
  re-seeded from the new image (Docker only seeds empty volumes). Either run
  `make collectstatic` after `make start`, or remove the volume first:
  `make down && docker volume rm accounts_static_files && make start`.
- Django logging the 404 means traffic is bypassing the `accounts-webserver`
  nginx container. Check on the production host that:
  - the `webserver` service is running (`docker compose ps`), and
  - the outer nginx-proxy routes `accounts2.bireme.org` to
    `accounts-webserver` (only it has `VIRTUAL_HOST`), not directly to the
    `accounts` container on port 8000.
