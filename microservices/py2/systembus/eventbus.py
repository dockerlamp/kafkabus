import random
import uuid
from copy import deepcopy
import asyncio
import json
import inspect
import importlib
import pkgutil

from kafka import KafkaProducer, KafkaConsumer


class EventBus:
    
    _kafka_producer = None
    _instance = None
    _kafka_consumer = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(EventBus, cls).__new__(cls)
        return cls._instance


    def __init__(self, bootstrap_servers, **kwargs):
        self._bootstrap_servers = bootstrap_servers


    def __enter__(self):
        if not EventBus._kafka_producer:
            EventBus._kafka_producer = KafkaProducer(bootstrap_servers = self._bootstrap_servers)
        return self


    def __exit__(self, type, value, traceback):
        if EventBus._kafka_producer:
            EventBus._kafka_producer.flush()
            EventBus._kafka_producer.close()
            EventBus._kafka_producer = None

        if EventBus._kafka_consumer:
            EventBus._kafka_consumer.close()
            EventBus._kafka_consumer = None


    def register_events(self, events_cfg):
        self._events_cfg = events_cfg


    async def register_event_handlers(self, handlers_package):
        self._handlers_registry = {}
        for _, module_name, _ in pkgutil.iter_modules(handlers_package.__path__):
            module = importlib.import_module(handlers_package.__name__ + '.' + module_name)
            for name, handler in inspect.getmembers(module, inspect.isfunction):
                self._handlers_registry[name] = handler

        return tuple(self._handlers_registry.keys())


    async def get_event_handler(self, name):
        return self._handlers_registry[name]


    async def valid(self, event):
        return True


    async def send(self, event, validate = True):
        topic_name = self._events_cfg[event['event_name']]['topic']
        topic_key = self._events_cfg[event['event_name']]['key']

        self.__enter__()
        EventBus._kafka_producer.send(topic =topic_name, \
            key = bytes(topic_key, 'utf-8') if topic_key else topic_key,\
                value = bytes(json.dumps(event), 'utf-8'))


    async def consume_from(self, topic, group):
        if not EventBus._kafka_consumer:
            EventBus._kafka_consumer = KafkaConsumer(bootstrap_servers = self._bootstrap_servers, group_id = group)
            EventBus._kafka_consumer.subscribe(topics = [topic])
        return EventBus._kafka_consumer
