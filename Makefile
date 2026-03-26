#!make

IMAGE_NAME=bireme/accounts
APP_VERSION=$(shell git describe --tags --long --always | sed 's/-g[a-z0-9]\{7\}//' | sed 's/-/./g')
TAG_LATEST=$(IMAGE_NAME):latest

## variable used in docker-compose for tag the build image
export IMAGE_TAG=$(IMAGE_NAME):$(APP_VERSION)

tag:
	@echo "IMAGE TAG:" $(IMAGE_TAG)
	@echo $(APP_VERSION) > app/templates/version.txt

COMPOSE_FILE_DEV=docker-compose-dev.yml

# docker compose commands
dev_build:
	@docker compose -f $(COMPOSE_FILE_DEV) build

dev_build_no_cache:
	@docker compose -f $(COMPOSE_FILE_DEV) build --no-cache

dev_run:
	@docker compose -f $(COMPOSE_FILE_DEV) up

dev_sh:
	@docker compose -f $(COMPOSE_FILE_DEV) exec accounts sh

dev_check:
	@docker compose -f $(COMPOSE_FILE_DEV) exec accounts sh -c "uv run --active manage.py check"

dev_makemigrations:
	@docker compose -f $(COMPOSE_FILE_DEV) exec accounts sh -c "uv run --active manage.py makemigrations"

dev_migrate:
	@docker compose -f $(COMPOSE_FILE_DEV) exec accounts sh -c "uv run --active manage.py migrate"

dev_test:
	@docker compose -f $(COMPOSE_FILE_DEV) exec accounts sh -c "uv run --active manage.py test --verbosity=2"

## PROD shortcuts
build:
	@docker compose build

build_no_cache:
	@docker compose build --no-cache

run:
	@docker compose up

start:
	@docker compose up -d

rm:
	@docker compose rm -f

logs:
	@docker compose logs -f

stop:
	@docker compose stop

down:
	@docker compose down

sh:
	@docker compose exec accounts sh

collectstatic:
	@docker compose exec -T accounts uv run manage.py collectstatic --noinput

migrate:
	@docker compose exec -T accounts uv run manage.py migrate
