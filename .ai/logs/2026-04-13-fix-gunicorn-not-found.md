# Fix production container deploy issues

## Problem
Running `make run` or `make start` failed with:
```
error: Failed to spawn: `gunicorn`
Caused by: No such file or directory (os error 2)
```

## Root cause
`gunicorn` is declared in the `prod` dependency group in `pyproject.toml`, but the Dockerfile builder stage ran `uv sync` without `--group prod`, so gunicorn was never installed into the virtualenv.

## Fix
Added `--group prod` to the `uv sync` command in the Dockerfile builder stage:
```dockerfile
RUN uv sync --frozen --no-install-project --active --group prod
```

## Problem 2
After fixing gunicorn install, gunicorn started but failed with:
```
ModuleNotFoundError: No module named 'accounts'
```

## Root cause
`COPY ./src /app/` copies the contents of `./src` into `/app/`, placing the `accounts` package at `/app/accounts/`. But `WORKDIR /app/src` set the working directory to a non-existent path, so Python couldn't find the module.

## Fix
Changed `WORKDIR /app/src` to `WORKDIR /app` in the prod stage.
