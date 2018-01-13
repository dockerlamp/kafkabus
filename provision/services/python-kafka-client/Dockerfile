FROM python:3.6-jessie

ARG librdkafka_version=0.11.3

ENV BOOTSTRAP_SERVERS=172.18.0.2:9092
ENV PYTHONUNBUFFERED=0

RUN curl -L https://github.com/edenhill/librdkafka/archive/v${librdkafka_version}.tar.gz | tar xzf - \
    && cd librdkafka-${librdkafka_version}/  \
    && ./configure --prefix=/usr \
    && make -j\
    && make install

RUN pip install confluent-kafka psutil
