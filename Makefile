#!make
include .env
# Export all variables (not commented lines) from .env file
$(eval export $(shell sed -ne 's/ *#.*$$//; /./ s/=.*$$// p' .env))

IMAGE_NAME=bireme/accounts
APP_VERSION=$(shell git describe --tags --long --always | sed 's/-g[a-z0-9]\{7\}//')
TAG_LATEST=$(IMAGE_NAME):latest

## variable used in docker-compose for tag the build image
export IMAGE_TAG=$(IMAGE_NAME):$(APP_VERSION)

tag:
	@echo "IMAGE TAG:" $(IMAGE_TAG)

## DEV shortcuts
dev_run:
	. ./set_env.sh && export && cd app && uv run manage.py runserver


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
