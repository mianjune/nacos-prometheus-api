FROM python:3.7-alpine

WORKDIR /data/nacos_prometheus_api

# Dependencies
COPY *.py requirements.txt ./
RUN pip install -r requirements.txt


ENTRYPOINT python run.py

