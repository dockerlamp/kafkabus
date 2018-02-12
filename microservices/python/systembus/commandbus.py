import json
import uuid
import random
from copy import deepcopy

from .ibus import IBus
from .kafkabus import KafkaBus

# platform settings
bus_config = json.load(open('../../systembus/bus.json'))

OBJECT_ID = random.randint(8*10**5, 9*10**5)


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
        command_ = deepcopy(command)
        uuid_ = str(uuid.uuid4())
        command_['uuid'] = uuid_

        topic_name = self.commands_config[command_['command_name']]['topic']
        topic_key = self.commands_config[command_['command_name']]['key']

        if topic_key != 'None':
            # command must be send with key to keep send order in kafka

            # TODO add dynamic object id to current topic key, e.g. "command.container.242345"
            # object id can identyfy container, stack or any object that command is related to 
            topic_key += '.'+str(OBJECT_ID)
        else:
            # command order in kafka not required (send to topic in round robin mode)
            topic_key = None

        self.__enter__() # ensure kafka producer is ready
        self._producer.send(topic = topic_name, key = bytes(topic_key, 'utf-8') if topic_key else topic_key,\
            value = bytes(json.dumps(command_), 'utf-8'))

        return uuid_


    async def consume_from(self, topic, group):
        # TODO use "channels" attrib from bus.json intead of topic and group?
        return await self._get_consumer(topic, group)


    async def get_handler(self, name):
        return self.command_handlers[name]
