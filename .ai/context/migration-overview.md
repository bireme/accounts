# Migration Overview: BIREME Accounts Django 5.2 Upgrade

This repository contains a migration of BIREME Accounts from legacy Django (code in `bireme/`) to Django 5.2 (code in `app/`). This file gives agents and contributors practical guidance to navigate, extend, and complete the migration.

Scope: This AGENTS.md applies to the entire repository.

## Project Map

- `app/` — New Django 5.2 project (Python 3.12, uv):
  - `accounts/` — Project settings, urls, wsgi/asgi.
  - `main/` — Migrated domain models, forms, views, admin, migrations.
  - `utils/` — Shared models (Generic, Country), admin, and utilities.
  - `manage.py` — Entry point for management commands.
  - `db.sqlite3` — Local development database (dev only).
- `bireme/` — Legacy Django project (originally 1.x; currently configured as 2.2). Use as reference only:
  - `accounts/` — Legacy settings and urls (includes `registration`, `api`, i18n, rosetta, static/templates dirs, etc.).
  - `main/`, `utils/`, `api/`, `registration/`, `templates/`, `static/`, `locale/` — Source of features to be migrated.
- `tasks/` — Migration plan and status:
  - `prd-django-migration.md` and `tasks-prd-django-migration.md` — Requirements + task checklist.
  - `chat-django-migration.md` — Work log and decisions.
- `docs/` — Local setup instructions.
- `Dockerfile`, `docker-compose.yml`, `docker-compose-dev.yml`, `Makefile` — Dev and prod tooling.
- `.env` — Dev environment variables (do not commit secrets elsewhere).

## Tooling & Versions

- Python: `>= 3.12` (configured via `pyproject.toml` and `.python-version`).
- Django: `>= 5.2`.
- Package manager: `uv` (see `Dockerfile` and `Makefile`).
- Key dependencies (`requirements.txt` / `pyproject.toml`):
  - `django-tastypie==0.15.1` (legacy API; verify Django 5.2 compatibility or plan DRF migration with feature parity).
  - `django-rosetta` (i18n UI; optional in prod).
  - `mysqlclient` (prod DB), `gunicorn`.

## Runbook

Dev (Docker):
- `make dev_run` — Runs app with hot-reload mounting `./app`.

Prod (Docker):
- `make run` — Builds (target: `prod`) and runs `app_accounts` + `nginx` proxy.
- Env file: `.env` (mounted by `docker-compose.yml`).
- Static files: `make collectstatic` (volume `static_files` served by nginx).

Notes:
- The Dockerfile `CMD` references `api_users.wsgi`; compose overrides with `accounts.wsgi`. If running the container directly, use `accounts.wsgi`.

## Environment Variables

New app (`app/accounts/settings.py`) expects:
- `APP_SECRET_KEY`, `APP_DEBUG`, `APP_ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`.
- Database: `DATABASE_ENGINE`, `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_HOST`, `DATABASE_PORT`.

Legacy (`bireme/accounts/settings.py`) used:
- `SECRET_KEY`, `DEBUG`, `DJANGO_ALLOWED_HOSTS`, etc.

Mapping guidance when porting configs:
- SECRET_KEY -> APP_SECRET_KEY
- DEBUG -> APP_DEBUG
- DJANGO_ALLOWED_HOSTS (or similar) -> APP_ALLOWED_HOSTS (comma-separated)
- Keep DB vars consistent across both for ease of switching.

`.env` contains sensible dev defaults; production uses `conf/app-env`.

## Migration Guidelines

General strategy:
- Treat `bireme/` as read-only reference. All new work belongs under `app/`.
- Port features incrementally, keeping the new project runnable at each step.
- Prefer minimal, compatible changes that preserve existing behavior.

Required modernizations when porting code:
- Imports: `ugettext_lazy` -> `gettext_lazy`; remove deprecated `RequestContext` usage.
- URLs: use `path()`/`re_path()`. Port legacy includes from `bireme/accounts/urls.py`.
- Models: ensure explicit `on_delete` in FK/OneToOne; use timezone-aware fields; keep names/relations stable to avoid schema drift.
- Middleware: include `LocaleMiddleware` for i18n if templates/i18n are used.
- Settings: add `LANGUAGES`, `LANGUAGE_CODE`, `TIME_ZONE`, `ITEMS_PER_PAGE` (used by views), and template DIRS for `BASE_DIR / "templates"`.
- Auth: port `utils.authenticate.EmailModelBackend` and add to `AUTHENTICATION_BACKENDS`.
- i18n: migrate `bireme/locale` to `app/locale` and ensure `django-rosetta` remains optional.
- Templates/Static: move from `bireme/templates` and `bireme/static` to `app/templates` and `app/static`; set `STATICFILES_DIRS` accordingly.
- API: confirm `django-tastypie` works with Django 5.2; otherwise replace with DRF endpoints that match request/response contracts.

Database & migrations:
- Use dev SQLite while migrating features; prod uses MySQL (`mysqlclient`).
- Initial migrations already exist for `main` and `utils`. After stabilizing models, `uv run manage.py makemigrations` should report "No changes detected".
- Avoid unintended schema changes; keep model field names and relations identical to legacy unless explicitly required by Django upgrades.

## URLs to Port (reference: `bireme/accounts/urls.py`)

- Include equivalents in `app/accounts/urls.py`:
  - `main.urls` at root (`^/`).
  - `registration.urls` at `^/accounts/`.
  - `api.urls` at `^/api/`.
  - i18n: `django.conf.urls.i18n` at `^/i18n/`.
  - utils cookie-lang: `utils.urls` at `^/cookie-lang/`.
  - Conditional rosetta at `^/rosetta/` when installed.

## How to Validate Changes

- `make dev_check` — Configuration sanity check.
- `make dev_makemigrations` — Should output "No changes detected" after initial migration.
- `make dev_migrate` — Apply migrations.
- `make dev_run` — Smoke test the server locally.
- Admin: ensure migrated models appear and work (`/admin/`).
- API: verify authentication and role endpoints behave like legacy.

## Coding Conventions

- Keep changes focused; do not modify `bireme/` except for reference.
- Python/Django style: follow PEP 8 and Django conventions.
- Use simple solutions; avoid over-engineering.
- Prefer f-strings and modern Python; no deprecated Django APIs.
- Keep files under ~300 lines where reasonable.
- Do not overwrite `.env`.
- Naming: Classes `PascalCase`; functions/vars `snake_case`; directories `kebab-case`; env vars `UPPER_SNAKE_CASE`.

## Useful Commands

- Run dev server: `make dev_run`
- Run migrations (dev): `make dev_migrate`
- Build prod image: `make build` (or `make build_no_cache`)
- Start prod stack: `make start`
- View logs: `make logs`
- Collect static (prod): `make collectstatic`


