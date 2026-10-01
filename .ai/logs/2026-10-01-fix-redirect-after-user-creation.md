# Fix redirect after user creation

## Problem
After creating a new user, the app redirected to `/users/edit/<id>//#!tab-permissions`
(double slash), which does not match the `users/edit/<int:user>/` route and returned 404.

## Cause
`reverse("main:edit_user", ...)` already returns a path with a trailing slash; the view
appended another `/` before the hash fragment.

## Change
- `src/main/views.py` (`new_user`): redirect now uses `"%s#!tab-permissions"`, producing
  `/users/edit/<id>/#!tab-permissions`. The existing JS in `edit-user.html` reads the
  `#!` hash and opens the Permissions tab.
- Same bug fixed for network creation: `"%s/#!tab-centers"` → `"%s#!tab-centers"`
  (`/network/edit/<id>/#!tab-centers`).
