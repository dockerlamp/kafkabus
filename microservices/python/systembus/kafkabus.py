import inspect
import importlib
import pkgutil
import asyncio
import uuid
import json

from kafka import KafkaProducer, KafkaConsumer

from ibus import IBus


class KafkaBus:
    
    _producer = None
    _consumers = {}


    def __init__(self, bus_config):
        self.bus_config = bus_config


    def __enter__(self):
        if not KafkaBus._producer:
            KafkaBus._producer = KafkaProducer(bootstrap_servers = self.bus_config['bootstrap_servers'])
        return self


    def __exit__(self, type, value, traceback):
        if KafkaBus._producer:
            KafkaBus._producer.flush()


    async def _get_consumer(self, topic, group):
        if (topic, group) not in self._consumers:
            new_consumer = KafkaConsumer(bootstrap_servers = self.bus_config['bootstrap_servers'], group_id = group)
            new_consumer.subscribe(topics = [topic])
            self._consumers[(topic, group)] = new_consumer
        return self._consumers[(topic, group)]


    @staticmethod
    def load_handlers(package):
        handlers = {}
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            module = importlib.import_module(package.__name__ + '.' + module_name)
            for name, handler in inspect.getmembers(module, inspect.isfunction):
                handlers[name] = handler
        return handlers
