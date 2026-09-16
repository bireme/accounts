# 2026-07-22 — Add `loaddata` Makefile target for XML fixture import

## Summary

Added a `make loaddata` target that imports a Django XML fixture (e.g.
`main.cooperativecenter` records) into the **running production** `accounts`
Docker container.

## Why

The app now runs in Docker. In production (`docker-compose.yml`) the source is
COPYed into the image with no bind mount (only `logs` / `static_files` volumes),
so a fixture sitting in the repo is not visible inside the running container. The
XML must be copied into the container before `manage.py loaddata` can read it.

## Change

`Makefile` — new variable and target next to the prod `migrate` / `collectstatic`
targets:

```makefile
## import fixture XML into the running (prod) accounts container
FILE ?= import/Centros.xml

loaddata:
	@docker compose cp $(FILE) accounts:/tmp/$(notdir $(FILE))
	@docker compose exec -T accounts uv run manage.py loaddata /tmp/$(notdir $(FILE))
	@echo "Imported $(FILE) into the running accounts container"
```

- `docker compose cp` copies the file into the running service container.
- Copied to `/tmp/<basename>` (writable by non-root `appuser`), extension
  preserved so Django auto-detects the XML serializer.
- Absolute path passed to `loaddata` so Django loads that exact file.
- Follows prod convention: `docker compose exec -T accounts uv run manage.py ...`.

## Usage

- Default file:  `make loaddata`
- Other fixture: `make loaddata FILE=import/backup/Centros_OK-20260622.xml`

## Verification

1. `make start` (prod stack up).
2. `make loaddata` → expect `Installed N object(s) from 1 fixture(s)`.
3. Spot check:
   `docker compose exec -T accounts uv run manage.py shell -c "from main.models import CooperativeCenter; print(CooperativeCenter.objects.filter(code='DO89.1').values('code','institution').first())"`
