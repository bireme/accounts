# Fix Change Language Option in Top Menu

Date: 2026-10-05
Branch: `feature/fix-change-language-option-in-top-menu`
Plan: [006-fix-change-language.md](../plans/006-fix-change-language.md)

## Problem

The language dropdown in the top menu set a cookie but never changed the interface. When the app moved to Django 5.2 and the legacy `bireme/` directory was removed (commit `ceb9eed`), the i18n setup was lost: `LocaleMiddleware`, `LANGUAGES`, `LOCALE_PATHS` and the `locale/` translation files. There were also smaller bugs: the menu sent `pt-BR` but compared against `pt-br`, the `next` field used an undefined variable, the form did nothing if the AJAX call failed, and `cookie_lang` accepted any value.

## Changes

- `src/accounts/settings.py`: added `LocaleMiddleware` after `SessionMiddleware`. Set `LANGUAGE_CODE = 'pt-br'`, set `LANGUAGES` to en, pt-br and es, and set `LOCALE_PATHS = [BASE_DIR / 'locale']`.
- `src/locale/{pt_BR,es}/LC_MESSAGES/django.{po,mo}`: restored unchanged from `ceb9eed^:bireme/locale/` (116 messages each).
- `src/templates/lang.html`: `next` now uses `{{ request.get_full_path }}`, and the form is submitted in `.always()` so a failed `cookie_lang` call doesn't block the switch.
- `src/templates/menu.html`: changed `change_language('pt-BR')` to `change_language('pt-br')`.
- `src/utils/views.py`: `cookie_lang` lowercases the code, checks it against `settings.LANGUAGES` (and returns 400 if it isn't there), and sets the cookie with Django's `LANGUAGE_COOKIE_*` settings. Removed the line that modified `request.COOKIES`, which had no effect.
- `Dockerfile`: the dev stage installs `gettext`. The prod stage is unchanged and uses the committed `.mo` files.
- `Makefile`: added the `dev_makemessages` (pt_BR, es) and `dev_compilemessages` targets.
- Tests:
  - `src/utils/tests/test_views.py`: `cookie_lang` lowercases the code and rejects invalid or missing values.
  - New `src/utils/tests/test_i18n.py`: covers the pt-br default, the redirect to `next` after the switch, the interface switching to es and en, the cookie taking precedence over Accept-Language, `cookie_lang` activating the language, the menu hiding the active language, and the `next` field holding the current path.

## Verification

- `make dev_check`: no issues.
- `make dev_test`: 199 tests, OK.
- `make dev_build`: the dev image builds and `msgfmt` 0.23.1 is available. Both restored `.po` files pass `msgfmt --check`.

## Follow-ups

- Strings added after 2015 have no translations yet. Run `make dev_makemessages`, translate, then `make dev_compilemessages`. The dev container must be recreated from the new image first.
- Anonymous pages (such as the login page) have no language switcher, because the menu only renders for authenticated users.

## Review notes

- A trial `makemessages` run shows the restored catalogs cover 109 of the 112 current strings. Untranslated: "User saved, but the activation email could not be sent. Check the server log.", "username or e-mail". Fuzzy (ignored by Django): "User successfully created.".
