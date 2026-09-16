# 005 — Log errors when email sending fails

## Context

Admins create/edit users in `src/main/views.py` (`new_user`, `edit_user` with `resend_email_flag`), which triggers Django's `PasswordResetForm.save()` to email the user a set-password link. Today:

- Any SMTP/backend exception propagates → HTTP 500 for the admin, nothing logged.
- `src/accounts/settings.py` never reads `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL` from the environment, so `.env.prod`'s SMTP config is silently ignored and Django falls back to `localhost:25` — the probable root cause of the failures.
- No `LOGGING` config exists; the project has no `logging` usage yet.
- Both views set `output['alert']` and then `redirect(...)`, so the "Activation email re-sent" alert is never actually shown.

Decisions taken with user: wire EMAIL_* env vars; log to console/stderr; use Django's messages framework for UI feedback; also cover the public password-reset flow.

## Implementation

### 1. `src/accounts/settings.py` — email config + LOGGING

- Add after `DATABASES` (or near the auth section):
  ```python
  # Email
  EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend' if TESTING else os.environ.get("EMAIL_BACKEND", 'django.core.mail.backends.smtp.EmailBackend')
  EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
  EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 25))
  EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
  EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
  EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "0").lower() in ("1", "true", "yes")
  EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "0").lower() in ("1", "true", "yes")
  EMAIL_TIMEOUT = int(os.environ.get("EMAIL_TIMEOUT", 10))
  DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "webmaster@localhost")
  SERVER_EMAIL = DEFAULT_FROM_EMAIL
  ```
  `EMAIL_TIMEOUT` matters: without it a dead SMTP host hangs the request until gunicorn's timeout.
- Add `LOGGING` dict: `version 1`, `disable_existing_loggers False`, a `verbose` formatter (`[%(asctime)s] %(levelname)s %(name)s: %(message)s`), one `console` handler on `StreamHandler`, root logger at `INFO`, plus loggers `django` (INFO) and `main`/`registration`/`utils` at `INFO`. Level overridable via `os.environ.get("LOG_LEVEL", "INFO")`.

### 2. New helper `src/utils/email.py`

Single place for the try/except so both views and the reset view share it:

```python
logger = logging.getLogger(__name__)

def send_password_setup_email(request, email):
    """Send Django's password-reset email; return True on success, False (and log) on failure."""
    form = auth_forms.PasswordResetForm({'email': email})
    if not form.is_valid():
        logger.warning("Password email not sent: invalid address %r", email)
        return False
    try:
        form.save(use_https=request.is_secure(), request=request)
    except Exception:  # SMTPException, socket.error, OSError, ...
        logger.exception("Failed to send password email to %s (triggered by %s)", email, request.user)
        return False
    return True
```

Catch broad `Exception`: SMTP failures surface as `smtplib.SMTPException`, `socket.gaierror`, `ConnectionRefusedError`, `TimeoutError` — all worth logging, none worth a 500.

### 3. `src/main/views.py` — use helper + messages

- `from django.contrib import messages` and `from utils.email import send_password_setup_email`.
- `edit_user` (~line 137): replace the inline `PasswordResetForm` block with
  ```python
  if resend_email == 'true':
      if send_password_setup_email(request, user.email):
          messages.success(request, _("Activation email re-sent"))
      else:
          messages.warning(request, _("User saved, but the activation email could not be sent. Check the server log."))
  ```
- `new_user` (~line 187): same pattern; `messages.success(request, _("User successfully created."))` on success, warning on failure. Keep `return redirect(...)` unchanged. Drop the now-dead `output['alert']` assignments before the redirects (leave the ones that render templates without redirecting untouched).

### 4. Templates — render messages after redirect

- `src/templates/alert.html`: extend to also loop `{% for message in messages %}` rendering the same `.box-alerts > .alert` markup with `alert-{{ message.tags }}` (map: success→`alert-success`, warning→`alert-warning`? — Bootstrap 2 uses `alert` (yellow) for warning, `alert-error`, `alert-success`, `alert-info`; set `MESSAGE_TAGS = {messages.ERROR: 'error'}` in settings so tags line up). Keep the existing `{% if alert %}` branch for views that still render inline.

### 5. `src/registration` — cover public "forgot password" flow

- `src/registration/views.py`: add `class LoggingPasswordResetView(auth_views.PasswordResetView)` overriding `form_valid` to wrap `super().form_valid(form)` in try/except, `logger.exception(...)` with the submitted email, then still `return redirect(self.get_success_url())` (Django intentionally does not reveal failures to anonymous users; we only add the log).
- `src/registration/urls.py:16`: swap `auth_views.PasswordResetView.as_view(...)` for the new class with the same `template_name`/`email_template_name`.

### 6. Tests (Django TestCase, run via `make dev_test`)

- `src/utils/tests/test_email.py` (new): with `self.assertLogs('utils.email', level='ERROR')` and `mock.patch('django.core.mail.EmailMultiAlternatives.send', side_effect=smtplib.SMTPException("boom"))` → returns False, log contains recipient; happy path → returns True and `len(mail.outbox) == 1`.
- `src/main/tests/test_views.py`: in `NewUserViewTest` and `EditUserViewTest`, add tests that patch the same send to raise, POST, assert `302`, user still saved, and a `messages.WARNING` in `get_messages(response.wsgi_request)`; add a success test asserting `mail.outbox` has 1 email and a success message for `resend_email_flag=true`.
- `src/registration/tests/test_views.py`: POST `/accounts/password/reset/` with send patched to raise → `302` to done page and `assertLogs('registration.views', 'ERROR')`.

### 7. Docs / housekeeping

- `.env.prod`/`.env.test` are untracked; note in the log file that they must use `KEY=value` (no spaces/quotes) for Docker `env_file` parsing — the current `.env.prod` has `EMAIL_HOST = '...'` which Compose will not parse as intended. Add commented `EMAIL_*` examples to `.env.dev` (also untracked, so mention in log for the user to apply).
- Write `.ai/logs/2026-09-16-log-email-send-errors.md` per CLAUDE.md.
- Copy this plan to `.ai/plans/005-log-email-send-errors.md` and link it from `.ai/current-feature.md` under `## Detailed Plan` (done at `/feature start` time since plan mode forbids other edits now).

## Verification

1. `make dev_test` — all existing tests plus the new ones pass.
2. Manual: in the dev container set `EMAIL_HOST=127.0.0.1 EMAIL_PORT=1` (nothing listening), create a user via `/users/new/` → redirect completes, yellow warning alert shows, `docker compose logs accounts` shows `ERROR utils.email: Failed to send password email to ... ` with traceback.
3. Manual: point `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend` → success message, email body printed in logs.
4. `/accounts/password/reset/` with broken SMTP → user still lands on "done" page, error logged.
