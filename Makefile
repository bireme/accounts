COMPOSE_FILE_DEV = docker-compose-dev.yml
COMPOSE_FILE_TEST = docker-compose-test.yml

export APP_BUILD_DATE=$(shell date -u +"%Y-%m-%dT%H:%M:%SZ")

build_date:
	@echo "Build date: " $(APP_BUILD_DATE)

## shortcuts docker-compose development
dev_compose_build:
	@docker-compose -f $(COMPOSE_FILE_DEV) build

dev_compose_up:
	@docker-compose -f $(COMPOSE_FILE_DEV) up -d

dev_compose_logs:
	@docker-compose -f $(COMPOSE_FILE_DEV) logs -f 

dev_compose_stop:
	@docker-compose -f $(COMPOSE_FILE_DEV) stop

dev_compose_ps:
	@docker-compose -f $(COMPOSE_FILE_DEV) ps

dev_compose_rm:
	@docker-compose -f $(COMPOSE_FILE_DEV) rm -f

dev_compose_exec_shell:
	@docker-compose -f $(COMPOSE_FILE_DEV) exec app sh

dev_compose_make_test:
	@docker-compose -f $(COMPOSE_FILE_DEV) exec app make test


## shortcuts docker-compose development
test_compose_build:
	@docker-compose -f $(COMPOSE_FILE_TEST) build

test_compose_up:
	@docker-compose -f $(COMPOSE_FILE_TEST) up -d

test_compose_logs:
	@docker-compose -f $(COMPOSE_FILE_TEST) logs -f 

test_compose_stop:
	@docker-compose -f $(COMPOSE_FILE_TEST) stop

test_compose_ps:
	@docker-compose -f $(COMPOSE_FILE_TEST) ps

test_compose_rm:
	@docker-compose -f $(COMPOSE_FILE_TEST) rm -f

test_compose_exec_shell:
	@docker-compose -f $(COMPOSE_FILE_TEST) exec app sh

test_compose_exec_collectstatic:
	@docker-compose -f $(COMPOSE_FILE_TEST) exec app python manage.py collectstatic --noinput

test_compose_make_test:
	@docker-compose -f $(COMPOSE_FILE_TEST) exec app make test

