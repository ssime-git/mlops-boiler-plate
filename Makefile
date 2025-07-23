init-airflow:
	mkdir -p ./dags ./logs ./plugins
	@echo AIRFLOW_UID=$(shell id -u) > .env
	docker compose up airflow-init

start:
	docker compose up -d

stop:
	docker compose down -v

restart:
	docker compose up --build

airflow-logs:
	docker-compose logs airflow-webserver

del-containers-and-images:
	docker stop $(docker ps -q)
	docker rm $(docker ps -aq)
	docker volume rm $(docker volume ls -q)

free-space:
	df -h