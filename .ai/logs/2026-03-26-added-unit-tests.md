# Added CRUD & List Unit Tests

## Date: 2026-03-26

## Summary

Implemented comprehensive unit tests for all 4 Django apps (main, utils, registration, api) covering CRUD operations, list views, models, forms, decorators, and API endpoints.

## Changes Made

### Infrastructure
- **`src/accounts/settings.py`**: Added fallback values for `SECRET_KEY` and `ALLOWED_HOSTS` to allow tests to run without env vars
- **`pyproject.toml`**: Added `dev` dependency group with `coverage~=7.6`
- **`Makefile`**:
  - Fixed `app_*` commands (`cd app` → `cd src`)
  - Added `app_deps_dev`, `app_test`, `app_test_coverage`, `dev_test` targets
  - `dev_test` overrides DB to SQLite in-memory for container testing

### Test Files Created
- **`src/accounts/test_helpers.py`**: Shared factory functions for creating test objects
- **`src/utils/tests/`**: test_models.py, test_views.py, test_authenticate.py
- **`src/main/tests/`**: test_models.py, test_views.py, test_forms.py, test_decorators.py
- **`src/registration/tests/`**: test_views.py, test_forms.py
- **`src/api/tests/`**: test_views.py, test_api.py

### Test Coverage
- **178 tests total**, all passing
- Models: Profile, Role, Service, RoleService, UserRoleService, CooperativeCenter, Topic, Network, NetworkMembership, Country, CountryLocal
- Views: Dashboard, Users CRUD/List, Networks CRUD/List, Services CRUD/List, Roles CRUD/List, ChangeProfile, Logout, API endpoints
- Forms: UserForm, NetworkForm, ServiceForm, RoleForm, ChangeProfileForm
- Decorators: @advanced_permission, @superuser_permission
- API: Tastypie UserResource login/logout, AJAX views (change_user_role_service, change_network_member, get_ccs, get_network_ccs)
- Auth: EmailModelBackend, cookie_lang view

## Bugs Discovered
- **`new_service` view**: Queries `RoleService.objects.filter(service=service)` with an unsaved Service instance on GET requests, raising `ValueError` in Django 5.2+. Tests document this with `assertRaises(ValueError)`.

## How to Run
```bash
make dev_test
```
