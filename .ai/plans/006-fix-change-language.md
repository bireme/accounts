# 006 — Fix Change Language Option in Top Menu

## Context

The language dropdown in the top menu (`src/templates/menu.html`) calls `change_language()` (`src/templates/lang.html`). That function sends an AJAX request to `utils:cookie_lang` and then submits Django's `set_language` form. The cookie gets set, but the interface never changes language. The Django 5.2 migration in commit `ceb9eed`, which removed the legacy `bireme/` directory, dropped the i18n setup the old app had:

- `django.middleware.locale.LocaleMiddleware` is not in `MIDDLEWARE`, so the language cookie is never read or activated.
- There are no `LANGUAGES` or `LOCALE_PATHS` settings.
- The `bireme/locale/{pt_BR,es}/LC_MESSAGES/django.{po,mo}` files were deleted, so no translations exist.

There are also smaller bugs: the menu sends `pt-BR` but compares against `pt-br`, the `next` hidden field uses an undefined `{{ redirect_to }}`, the form never submits if the AJAX call fails, and `cookie_lang` stores any value it receives without validation.

Intended outcome: choosing English, Português or Español in the menu immediately reloads the current page in that language, and the choice persists through the cookie.

## Decisions (from clarification)

- **Translations:** restore the old `.po`/`.mo` files from git history as they are. No makemessages pass now.
- **Persistence:** keep the `cookie_lang` AJAX view, but validate and normalize its input.
- **Default language:** `pt-br`. Accept-Language and the cookie still take precedence through LocaleMiddleware.
- **.mo files:** commit them. Install gettext only in the dev image and add Makefile targets for future translation work.

## Implementation Steps

### 1. Settings — `src/accounts/settings.py`
- Add `'django.middleware.locale.LocaleMiddleware'` after `SessionMiddleware` and before `CommonMiddleware`, which is the order Django requires.
- `LANGUAGE_CODE = 'pt-br'`
- Add `LANGUAGES = [('en', 'English'), ('pt-br', 'Português'), ('es', 'Español')]`. Use lowercase `pt-br` to match `utils.models.LANGUAGES_CHOICES` and the `*Local.language` values.
- Add `LOCALE_PATHS = [BASE_DIR / 'locale']`, which resolves to `src/locale/`.

### 2. Restore translations
- Restore `src/locale/pt_BR/LC_MESSAGES/django.{po,mo}` from `ceb9eed^:bireme/locale/pt_BR/...` and `src/locale/es/LC_MESSAGES/django.{po,mo}` from `ceb9eed^:bireme/locale/es/...` with `git show ceb9eed^:<path> > <dest>`.
- Leave the `#:` source references alone. They are cosmetic and get refreshed on the next makemessages run.

### 3. JS switcher — `src/templates/lang.html`
- Set `next` to `{{ request.get_full_path }}`. The request context processor is already enabled.
- Submit the form in `.always()` instead of the success callback, so a failed `cookie_lang` call doesn't block the switch.
- Keep the `$.get` call to `utils:cookie_lang`, because the user chose to keep it.

### 4. Menu — `src/templates/menu.html`
- Change `change_language('pt-BR')` to `change_language('pt-br')`, so all codes match `LANGUAGES` and the existing `LANGUAGE_CODE == 'pt-br'` checks.

### 5. `cookie_lang` view — `src/utils/views.py`
- Normalize the input with `.lower()` and reject values that aren't in `dict(settings.LANGUAGES)`. Return `HttpResponseBadRequest` without setting the cookie.
- Set the cookie with Django's language-cookie settings (`max_age=settings.LANGUAGE_COOKIE_AGE`, `path`, `domain`, `secure`, `httponly`, `samesite` from `settings.LANGUAGE_COOKIE_*`) so it matches what `set_language` writes.
- Remove the no-op `request.COOKIES[...] = language` mutation, but keep the session write so existing behavior and tests stay intact.

### 6. Docker and Makefile
- `Dockerfile` dev stage: add `gettext` to the `apt-get install` list. The prod stage is unchanged.
- `Makefile`: add `dev_makemessages` (`manage.py makemessages -l pt_BR -l es`) and `dev_compilemessages` (`manage.py compilemessages`), following the `dev_*` pattern.

### 7. Tests
- `src/utils/tests/test_views.py`: add a case where an invalid language returns 400 and sets no cookie, and a case where uppercase `pt-BR` is normalized to `pt-br`.
- New i18n tests, for example in `src/utils/tests/test_i18n.py`:
  - POSTing `/i18n/setlang/` with `language=es` and `next=/` redirects to `/`, and later requests render Spanish (`Content-Language: es`, plus a known translated string such as the `Dashboard` / `Users` menu label).
  - When there is no cookie and no Accept-Language header, the response language is `pt-br`.
  - The `es` cookie wins over an `Accept-Language: en` header.
  - The menu for an authenticated user doesn't offer the active language and does offer the other two.

## Critical Files
- `src/accounts/settings.py`
- `src/templates/lang.html`, `src/templates/menu.html`
- `src/utils/views.py`, `src/utils/tests/test_views.py`, plus the new `src/utils/tests/test_i18n.py`
- `src/locale/**` (restored)
- `Dockerfile`, `Makefile`

## Verification
1. `make dev_build`, then `make dev_run`. A rebuild is needed for gettext.
2. `make dev_check` should report no issues.
3. `make dev_test` should pass, including the new tests.
4. Manual check: log in, switch through each language in the menu, and confirm the page reloads on the same URL with translated labels, the active language is hidden from the dropdown, and the choice survives a browser restart.
5. `make dev_compilemessages` should run inside the container, which confirms gettext is installed.
6. Write `.ai/logs/2026-10-05-fix-change-language.md` and update `.ai/current-feature.md`.
