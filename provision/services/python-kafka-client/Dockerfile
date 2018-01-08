FROM python:alpine3.6

ARG kafka_topic_name=simple_topic
ARG bootstrap_servers=172.18.0.2:9092

ENV KAFKA_TOPIC_NAME=$kafka_topic_name
ENV BOOTSTRAP_SERVERS=$bootstrap_servers
ENV PYTHONUNBUFFERED=0

RUN apk --update add gcc musl-dev linux-headers

RUN pip install kafka-python psutil watchdog
