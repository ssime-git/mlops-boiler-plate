.SILENT:
.PHONY: help

done = printf "\e[32m ✔ Done\e[0m\n\n";

## This help screen
help:
	printf "Available commands\n\n"
	awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "\033[33m%-40s\033[0m %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

## Initialize Airflow
init-airflow:
	mkdir -p ./dags ./logs ./plugins
	@echo AIRFLOW_UID=$(shell id -u) > .env
	docker compose up airflow-init
	$(done)
.PHONY: init-airflow

## Start Containers
start:
	docker compose up -d --force-recreate
	$(done)
.PHONY: start

## Stop Containers
stop:
	docker compose down
	$(done)
.PHONY: stop

## Restart Containers
rebuild:
	docker compose down
	docker compose up --build
	docker compose up -d --force-recreate
	$(done)
.PHONY: rebuild

## Show Airflow Logs
airflow-logs:
	docker-compose logs airflow-webserver
	$(done)
.PHONY: airflow-logs

## Remove all containers and volumes
remove:
	docker stop $(docker ps -q)
	docker rm $(docker ps -aq)
	docker volume rm $(docker volume ls -q)
	$(done)
.PHONY: remove

## Show disk space
free-space:
	df -h
	$(done)
.PHONY: free-space