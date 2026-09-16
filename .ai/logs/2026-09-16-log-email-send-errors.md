# 2026-09-16 — Log errors when email sending fails

Feature branch: `feature/log-email-send-errors` · Plan: `.ai/plans/005-log-email-send-errors.md`

## Problem

Admins creating/editing users (`/users/new/`, `/users/edit/<id>/` with *resend activation*)
trigger a password-setup email. When SMTP failed nothing was logged and the admin got no
feedback. Root causes found while implementing:

1. `src/accounts/settings.py` never read `EMAIL_HOST` / `EMAIL_PORT` / `EMAIL_HOST_USER` /
   `EMAIL_HOST_PASSWORD` / `EMAIL_USE_TLS` / `DEFAULT_FROM_EMAIL` from the environment, so the
   values in `.env.prod` were ignored and Django tried `localhost:25`.
2. No `LOGGING` config. Django 5.2 already catches the SMTP exception inside
   `PasswordResetForm.send_mail()` and logs to `django.contrib.auth`, but with `DEBUG=0` and the
   default logging config that message went nowhere.
3. Both admin views set `output['alert']` and then `redirect()`, so the "Activation email re-sent"
   alert was never displayed.
4. The public "forgot password" form (`/accounts/password/reset/`) returned HTTP 500 on every
   submit: Django's `PasswordResetView.success_url` reverses `password_reset_done` but the project
   names the route `auth_password_reset_done` (same for the confirm → complete step).

## Changes

- `src/accounts/settings.py`
  - `EMAIL_*` settings read from env (`EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`,
    `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `EMAIL_USE_SSL`, `EMAIL_TIMEOUT`=10s, `DEFAULT_FROM_EMAIL`).
    Tests use the `locmem` backend.
  - `LOGGING`: single console/stderr handler, root + `django` + app loggers at `LOG_LEVEL` (env, default `INFO`).
    Shows up in `docker compose logs accounts`.
  - `MESSAGE_TAGS` so `messages.error` maps to Bootstrap 2's `alert-error`.
- `src/utils/email.py` (new)
  - `StrictPasswordResetForm`: same as Django's but `send_mail()` re-raises instead of swallowing.
  - `send_password_setup_email(request, email)`: sends the set-password email, returns `True`/`False`,
    logs `logger.exception(...)` with recipient + the admin who triggered it on failure.
- `src/main/views.py`: `edit_user` / `new_user` use the helper and the Django messages framework
  (`messages.success` / `messages.warning`) so feedback survives the redirect.
- `src/templates/alert.html`: renders `messages` in addition to the legacy `alert` context var.
- `src/registration/views.py` + `urls.py`: `PasswordResetView` subclass (strict form, logs failures with
  the address, correct `success_url`); `PasswordResetConfirmView` subclass with correct `success_url`.
- Tests: `src/utils/tests/test_email.py` (new), new cases in `src/main/tests/test_views.py` and
  `src/registration/tests/test_views.py` — mock `EmailMultiAlternatives.send` raising `SMTPException`,
  assert log output, HTTP 302, user persisted, warning message. Full suite: 189 tests OK.

## Action required on deploy (untracked env files)

`.env.prod` currently has the email block as `EMAIL_HOST = 'esmeralda04.bireme.br'` (spaces + quotes).
Docker Compose `env_file` does not parse that form as intended — normalise to `KEY=value`:

```
EMAIL_HOST=esmeralda04.bireme.br
EMAIL_PORT=587
EMAIL_HOST_USER=contato@bireme.org
EMAIL_HOST_PASSWORD=...
EMAIL_USE_TLS=1
DEFAULT_FROM_EMAIL=contato@bireme.org
# optional
# EMAIL_TIMEOUT=10
# LOG_LEVEL=INFO
```

For local dev, `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend` in `.env.dev` prints
emails to the container log instead of sending.

## Out of scope / noticed

- `PasswordChangeView` (`/accounts/password/change/`) has the same `success_url` name mismatch
  (`password_change_done` vs `auth_password_change_done`) — not touched here.
- `src/templates/main/edit-user.html` had an unrelated uncommitted change (multiple-select widget on
  `#id_cc`) already present in the working tree before this feature; left as is.
