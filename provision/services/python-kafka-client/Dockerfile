FROM python:3.6-jessie

ARG bootstrap_servers=172.18.0.2:9092

ENV BOOTSTRAP_SERVERS=$bootstrap_servers
ENV PYTHONUNBUFFERED=0

RUN pip install kafka-python psutil
