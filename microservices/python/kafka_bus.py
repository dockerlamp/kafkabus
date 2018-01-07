import os
from kafka import KafkaConsumer, KafkaProducer

BOOTSTRAP_SERVERS = os.environ['BOOTSTRAP_SERVERS']

class MessageBusError(Exception):
    pass


class KafkaBus():
    def __init__(self, bootstrap_servers):
        self._bootstrap_servers = bootstrap_servers


    def consume_from(self, topic, **kwargs):
        consumer = KafkaConsumer(bootstrap_servers= self._bootstrap_servers, **kwargs)
        available_topics = consumer.topics()
        if topic not in available_topics:
            raise MessageBusError('Requested channel %s not found in message bus.' % topic)
        consumer.subscribe(topics = [topic])
        return consumer


    def produce_to(self, **kwargs):
        producer = KafkaProducer(bootstrap_servers= self._bootstrap_servers, **kwargs)
        return producer

message_bus = KafkaBus(BOOTSTRAP_SERVERS)
