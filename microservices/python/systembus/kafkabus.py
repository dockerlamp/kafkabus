import inspect
import importlib
import pkgutil
import asyncio
import uuid
import json

from ibus import IBus


class KafkaBus:
    
    _producer = None
    _consumers = {}


    def __init__(self, bus_config):
        self.bus_config = bus_config


    async def __aenter__(self):
        return self


    async def __aexit__(self, type, value, traceback):
        if KafkaBus._producer:
            KafkaBus._producer.flush()


    @staticmethod
    def load_handlers(package):
        handlers = {}
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            module = importlib.import_module(package.__name__ + '.' + module_name)
            for name, handler in inspect.getmembers(module, inspect.isfunction):
                handlers[name] = handler
        return handlers
