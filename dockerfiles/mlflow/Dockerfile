FROM python:3.9-slim-bullseye@sha256:b9e06687fbfc57f6fe563e94e4c8751e39513dde89afc120dc6f56afe5ffc761
# Install python packages
RUN apt-get update
RUN apt-get install -y postgresql postgresql-contrib postgresql-server-dev-all
RUN pip install mlflow boto3 pymysql psycopg2-binary 
