import json

from ibus import IBus
from kafkabus import KafkaBus

# platform settings
bus_config = json.load(open('../../../systembus/bus.json'))
commands_config = json.load(open('../../../systembus/commands.json'))


class CommandBus(IBus, KafkaBus):
    '''singleton'''
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CommandBus, cls).__new__(cls)
        return cls._instance


    def __init__(self, commands_config = None):
        super().__init__(bus_config)
        if commands_config:
            self.commands_config = commands_config

        if not hasattr(self, 'command_handlers'):
            self.command_handlers = {}


    async def add_handler(self, name, command_handler):
        if name in self.command_handlers:
            raise ValueError('Command handler %s already registered!')
        self.command_handlers[name] = command_handler


    async def send(self, command):
        pass


    async def consume_from(self, topic, group):
        pass
