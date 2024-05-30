start:
	docker compose up

restart:
	docker compose up --build

airflow-logs:
	docker-compose logs airflow-webserver

setup-airflow:
	mkdir -p ./dags ./logs ./plugins
	echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
	docker compose up airflow-init