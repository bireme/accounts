# Plan: Implement CRUD & List Unit Tests for All Django Apps

## Context

The project has 4 Django apps (`main`, `utils`, `registration`, `api`) with zero test coverage — all `tests.py` files are empty stubs. The goal is to add comprehensive unit tests for CRUD operations, list views, models, forms, decorators, and API endpoints using Django's built-in `TestCase`. This will establish a solid testing foundation for the project.

---

## Pre-requisites (Infrastructure)

### 1. Fix settings for test runner (`src/accounts/settings.py`)
Lines 24 and 29 will crash without env vars. Add safe fallbacks:
- `SECRET_KEY`: fallback to a test-only key
- `ALLOWED_HOSTS`: fallback to `"localhost,127.0.0.1"`

### 2. Add test dependencies (`pyproject.toml`)
Add a `dev` dependency group:
```toml
[dependency-groups]
dev = ["coverage~=7.6"]
```
Run `uv sync --group dev` to install.

### 3. Fix and add Makefile commands (`Makefile`)
- **Fix**: Existing `app_*` commands use `cd app` but the source is in `src/` — fix all to `cd src`
- **Add** test targets:
  - `app_test` — run all tests locally
  - `app_test_coverage` — run tests with coverage report
  - `dev_test` — run tests inside Docker dev container

### 4. Create shared test helpers (`src/accounts/test_helpers.py`)
Factory functions for creating test objects (users, profiles, countries, CCs, roles, services, networks). Every test file imports from here to avoid duplication.

---

## Test Structure

Convert each app's `tests.py` into a `tests/` package:

```
src/
  accounts/
    test_helpers.py          # Shared factory functions
  main/
    tests/
      __init__.py
      test_models.py         # ~9 classes, ~28 methods
      test_views.py          # ~12 classes, ~58 methods
      test_forms.py          # ~4 classes, ~16 methods
      test_decorators.py     # ~2 classes, ~8 methods
  utils/
    tests/
      __init__.py
      test_models.py         # ~3 classes, ~8 methods
      test_views.py          # ~1 class, ~3 methods
      test_authenticate.py   # ~1 class, ~5 methods
  registration/
    tests/
      __init__.py
      test_views.py          # ~2 classes, ~6 methods
      test_forms.py          # ~1 class, ~4 methods
  api/
    tests/
      __init__.py
      test_views.py          # ~4 classes, ~18 methods
      test_api.py            # ~2 classes, ~10 methods
```

**Total: ~41 test classes, ~164 test methods**

---

## Detailed Test Coverage Per App

### `utils` App

**test_models.py** — Country, CountryLocal, Generic behavior
- Create/read Country, verify fields and `__str__`
- Verify `updated` timestamp changes on re-save (Generic.save override)
- CountryLocal cascade delete when Country deleted

**test_views.py** — cookie_lang view
- Sets language cookie, updates session, returns language string

**test_authenticate.py** — EmailModelBackend
- Authenticate with email (success, wrong password, nonexistent)
- `get_user` (existing, nonexistent)

### `main` App

**test_models.py** — All main models
- Profile: auto-creation via signal, default type, `is_basic()`/`is_advanced()`, `get_role_services()`
- Role, Service, RoleService, UserRoleService: create, `__str__`, FK constraints (CASCADE vs PROTECT)
- CooperativeCenter: create, unique code constraint
- Network: create, `list_members()`, type choices
- NetworkMembership: create, verify FKs

**test_decorators.py** — Permission decorators
- `@advanced_permission`: basic user → 404, advanced → 200, superuser → 200, anon → redirect
- `@superuser_permission`: basic → 404, advanced → 404, superuser → 200, anon → redirect

**test_forms.py** — All main forms
- UserForm: valid/invalid data, save updates Profile type/CC, superuser vs advanced user field differences
- NetworkForm: valid/invalid, responsible queryset ordering
- ServiceForm, RoleForm: valid/invalid field combinations

**test_views.py** — All CRUD and list views

| Entity | List | Create (GET+POST) | Edit (GET+POST) | Permissions |
|--------|------|--------------------|------------------|-------------|
| Users | search, filter by CC, pagination, ordering | superuser + advanced | superuser + advanced | @advanced_permission |
| Networks | search, ordering | superuser + advanced | superuser + advanced | @advanced_permission |
| Services | search, ordering | superuser only | superuser only, role associations | @superuser_permission |
| Roles | search, ordering | superuser only | superuser only | @superuser_permission |
| Dashboard | — | — | — | redirect basic → change_profile |

Each view tests: unauthenticated redirect, permission denied (404), successful GET (form in context), successful POST (object created/updated, redirect), invalid POST (form errors), nonexistent ID (404).

### `registration` App

**test_views.py**
- `change_profile`: GET renders form, POST updates email, unauthenticated redirects
- `logout_view`: renders template, actually logs user out

**test_forms.py**
- ChangeProfileForm: valid/invalid, only email field, save updates user email

### `api` App

**test_views.py** — AJAX and JSON endpoints
- `change_user_role_service`: add (checked=true), remove (checked=false), duplicate prevention, invalid IDs → 404
- `change_network_member`: add/remove members, invalid IDs → 404
- `get_ccs`: filter by code, country, network context (note: `@login_required`)
- `get_network_ccs`: returns JSON with member codes, no auth required, nonexistent network → 404

**test_api.py** — Tastypie UserResource
- Login: success, wrong password, inactive user, no CC, service filter, method not allowed
- Logout: success, unauthenticated, method not allowed

---

## Implementation Order

1. Settings fallbacks (`src/accounts/settings.py`)
2. `pyproject.toml` dev deps + `uv sync --group dev`
3. Makefile fixes and test commands
4. Shared test helpers (`src/accounts/test_helpers.py`)
5. `utils` tests (smallest app, validates infrastructure)
6. `main/tests/test_models.py`
7. `main/tests/test_decorators.py`
8. `main/tests/test_forms.py`
9. `main/tests/test_views.py` (largest file)
10. `registration` tests
11. `api` tests
12. Run `make app_test` — verify all pass
13. Create log file `.ai/logs/2026-03-26-added-unit-tests.md`

---

## Verification

1. `make app_test` — all ~164 tests pass with 0 failures
2. `make app_test_coverage` — generate coverage report, aim for >85% on view/model code
3. Verify tests run without env vars (SQLite default, fallback settings)

---

## Key Decisions

- **Django TestCase only** — no pytest, no factory_boy; factory functions in `test_helpers.py` suffice
- **SQLite for tests** — settings already default to SQLite, no MySQL needed
- **No template content assertions** — test status codes, redirects, context, and template names only
- **Fix Makefile `cd app` → `cd src`** — existing commands are broken since the rename refactor
