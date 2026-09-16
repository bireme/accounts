# 2026-07-23 — Fix `make loaddata` PermissionError (stream fixture via stdin)

## Problem

After deploying [2026-07-22-add-loaddata-makefile-target](2026-07-22-add-loaddata-makefile-target.md),
`make loaddata` failed in production:

```
PermissionError: [Errno 13] Permission denied: '/tmp/Centros.xml'
```

The `docker compose cp` step succeeded ("Copied"), so the failure was not the copy.

## Root cause

`docker compose cp` writes the destination file as **root**, preserving the host
file's mode. The image runs as the non-root `appuser` (`Dockerfile:58`, `Dockerfile:90`),
so `manage.py loaddata` opened `/tmp/Centros.xml` as UID 1000 and was denied —
the file was root-owned without read permission for others (restrictive source
mode, or a stale root-owned `/tmp/Centros.xml` left by an earlier run). The
target never adjusted ownership/mode after copying.

## Change

`Makefile` — removed the temp-file copy and stream the fixture into the container
over stdin instead. Django 5.2 accepts `-` as a fixture label when `--format` is
given, and `docker compose exec -T` already provides a non-TTY stdin:

```makefile
## import fixture XML into the running (prod) accounts container
FILE ?= import/Centros.xml

loaddata:
	@docker compose exec -T accounts uv run manage.py loaddata --format=xml - < $(FILE)
	@echo "Imported $(FILE) into the running accounts container"
```

Benefits: no file written inside the container, so no ownership/permission
handling, no stale-file risk, and no `exec -u root` privileged step.

Trade-off: the serializer is pinned to `xml` rather than inferred from the file
extension. All fixtures under `import/` are XML. If a non-XML fixture is ever
needed, use `--format=$(subst .,,$(suffix $(FILE)))`.

## Usage (unchanged)

- Default file:  `make loaddata`
- Other fixture: `make loaddata FILE=import/backup/Centros_OK-20260622.xml`

## Verification

1. `make start` (prod stack up).
2. `make loaddata` → expect `Installed N object(s) from 1 fixture(s)`.
3. Spot check:
   `docker compose exec -T accounts uv run manage.py shell -c "from main.models import CooperativeCenter; print(CooperativeCenter.objects.filter(code='DO89.1').values('code','institution').first())"`

Not verified locally: this repo checkout has no `import/Centros.xml` and the prod
stack is not running here, so the target was not executed — it needs a run on the
deploy host.
