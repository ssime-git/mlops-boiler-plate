FROM python:3.11-slim

WORKDIR /usr/src/app

COPY app.py app.py
COPY score score
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
