# Current Feature: Log error messages when fail to send email

## Status

Not Started

## Goals

- Wrap the email-sending calls (`PasswordResetForm.save()` in `src/main/views.py` `edit_user` and `new_user`, plus the password-reset flow in `registration`) in error handling so an SMTP/backend failure does not crash the request
- Log the exception with `logging` (module logger, `logger.exception`/`logger.error`) including recipient email and context (which view/action triggered the send)
- Show the admin a clear warning alert in the UI when the email could not be sent (instead of the "Activation email re-sent" success message)
- Ensure `LOGGING` is configured in `src/accounts/settings.py` so these errors reach a handler (console/file) in production
- Add tests that simulate a send failure (e.g. mock `send_mail`/backend raising `SMTPException`) and assert the error is logged and the request still succeeds

## Notes

- Inline description (no spec file in `.ai/features/`)
- Email is currently sent through Django's `auth_forms.PasswordResetForm.save()` at `src/main/views.py:145` (edit_user, resend flag) and `src/main/views.py:194` (new_user). Neither call has error handling today.
- No `LOGGING` setting exists in `src/accounts/settings.py`; the project also has no `logging.getLogger` usage yet — a new logger convention will be introduced.
- Keep the user-facing behaviour: user is still saved even if the email fails; only the alert changes.

## Detailed Plan

[005-log-email-send-errors.md](.ai/plans/005-log-email-send-errors.md)

## History

