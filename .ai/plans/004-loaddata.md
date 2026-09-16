# Plan: Add a Makefile task to import the CooperativeCenter XML fixture into the running Docker container

## Context

The system imports `main.cooperativecenter` records from a Django XML fixture
(`import/Centros_OK.xml`). The fixture is fetched from a remote server by
`import/update-centros-nmail.sh` and matches the structure in the request
(`<object model="main.cooperativecenter">` with `code` / `country` / `institution`).

Previously the import ran directly on the host with `manage.py loaddata`. Now the
app runs in Docker. In **production** (`docker-compose.yml`) the source code is
COPYed into the image (WORKDIR `/app`) and there is **no bind mount** — only
`logs` and `static_files` volumes. So a fixture sitting in the repo is **not**
visible inside the running container and must be copied in before `loaddata` can
read it.

Goal: add a Makefile target that copies the XML into the running `accounts`
container and runs `loaddata` against it, following the existing prod Makefile
conventions.

Decisions (confirmed with user): **prod only**; default to `import/Centros.xml`,
overridable via `FILE=...`.

## Implementation

### File to modify: `Makefile`

Add near the other prod manage.py targets (`migrate`, `collectstatic`). The prod
convention is `docker compose exec -T accounts uv run manage.py <cmd>` (service
name `accounts`, container_name also `accounts`).

Add a variable and target:

```makefile
## import fixture XML into the running (prod) accounts container
FILE ?= import/Centros.xml

loaddata:
	@docker compose cp $(FILE) accounts:/tmp/$(notdir $(FILE))
	@docker compose exec -T accounts uv run manage.py loaddata /tmp/$(notdir $(FILE))
	@echo "Imported $(FILE) into the running accounts container"
```

Notes:
- `docker compose cp` copies from the host into the running service container
  (Compose v2), keeping it consistent with the rest of the Makefile which uses
  `docker compose ...`.
- Copy target is `/tmp/<basename>` — `/tmp` is writable by the non-root
  `appuser` (uid 1000), and preserving the `.xml` extension lets Django's
  `loaddata` auto-detect the XML serializer.
- `loaddata` is given an absolute path (`/tmp/Centros.xml`), so Django loads
  that exact file rather than searching app `fixtures/` dirs (there are none).
- Prod target mirrors `migrate`/`collectstatic`: `uv run manage.py` (no
  `--active`) with `-T` to avoid TTY allocation.

### Usage
- Default file:  `make loaddata`
- Other fixture: `make loaddata FILE=import/Centros_20260622.xml`

## Verification

1. Ensure the prod stack is running: `make start` (or `make run`).
2. Run `make loaddata`.
3. Expect Django output like `Installed N object(s) from 1 fixture(s)` and the
   final echo line.
4. Spot-check the data landed:
   `docker compose exec -T accounts uv run manage.py shell -c "from main.models import CooperativeCenter; print(CooperativeCenter.objects.filter(code='DO89.1').values('code','institution').first())"`
5. Negative check for the copy step:
   `docker compose exec -T accounts ls -l /tmp/Centros.xml` should show the file.

## Post-implementation

Per `CLAUDE.md`, create a log file
`.ai/logs/2026-07-22-add-loaddata-makefile-target.md` summarizing the change.
