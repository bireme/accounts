# Fix production gunicorn startup error

**Date:** 2026-04-09

## Problem

The production container failed to start with:

```
error: Failed to spawn: `gunicorn`
Caused by: No such file or directory (os error 2)
```

## Root Cause

The production stage `CMD` in `Dockerfile` (line 96) was missing the `--active` flag on the `uv run` command. Without `--active`, `uv` does not use the existing virtual environment at `/.venv`, so it cannot locate the `gunicorn` binary installed there.

The dev stage already had the correct `--active` flag, but the prod stage did not.

## Fix

Added `--active` to the production `CMD`:

```diff
- CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "accounts.wsgi:application"]
+ CMD ["uv", "run", "--active", "gunicorn", "--bind", "0.0.0.0:8000", "accounts.wsgi:application"]
```
