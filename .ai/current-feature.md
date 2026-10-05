# Current Feature: Fix Change Language Option in Top Menu

## Status

Completed

## Goals

- Picking English / Portuguese / Spanish in the top menu dropdown changes the interface language right away
- The chosen language persists across requests and new visits (session/cookie), for both anonymous and logged-in users
- After switching, the user returns to the page they were on (correct `next` redirect)
- The menu only lists the languages other than the active one (`LANGUAGE_CODE` comparisons match the configured codes)
- Translations for pt-BR and es exist and are compiled so the switch actually shows translated text
- Tests cover the language switch flow

## Notes

Inline feature description: "Fix change language option available in the top menu that use a javascript to change the interface language of the system."

Current implementation (findings while loading):
- `src/templates/menu.html:35-37` — links call `change_language('en' | 'pt-BR' | 'es')`
- `src/templates/lang.html` — JS does `$.get` to `utils:cookie_lang`, then submits a hidden form to Django's `set_language`; `next` uses `{{ redirect_to }}`, which is probably never set in context
- `src/utils/views.py` `cookie_lang` — sets a cookie + session key with the raw value (no validation)
- `src/accounts/urls.py:36-37` — `i18n/` (Django `set_language`) and `cookie-lang/` are both wired
- `src/accounts/settings.py` — **no `LocaleMiddleware`**, no `LANGUAGES`, no `LOCALE_PATHS`; `LANGUAGE_CODE = 'en-us'`, so the menu check `LANGUAGE_CODE != "en"` is always true
- No `locale/` directory or `.po`/`.mo` files in the repo, so translations don't exist yet
- Code mismatch: menu uses `pt-BR`, template compares `pt-br`, `utils.models.LANGUAGES_CHOICES` uses `pt-br`
- Root cause: the Django migration (commit `ceb9eed`) dropped `LocaleMiddleware`, `LANGUAGES`, `LOCALE_PATHS` and `bireme/locale/` (pt_BR, es `.po`/`.mo`)
- Decisions: restore old translations as-is; keep `cookie_lang` (validated); default `pt-br`; commit `.mo`, gettext in dev image only. Existing tests are in `src/utils/tests/test_views.py`

## Detailed Plan

[006-fix-change-language.md](.ai/plans/006-fix-change-language.md)

## History

- 2026-09-16: Starting Log error messages when fail to send email — following plan [005-log-email-send-errors.md](.ai/plans/005-log-email-send-errors.md)
- 2026-09-16: Completed Log error messages when fail to send email — email failures logged (`utils.email`, `registration.views`) with recipient/context, admin sees warning via messages framework, `EMAIL_*` env + `LOGGING` in settings, public reset flow success_url fixed. Log: [2026-09-16-log-email-send-errors.md](.ai/logs/2026-09-16-log-email-send-errors.md)
- 2026-10-05: Starting Fix Change Language Option in Top Menu — following plan [006-fix-change-language.md](.ai/plans/006-fix-change-language.md)
