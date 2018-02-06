import random
import uuid
from copy import deepcopy
import asyncio
import json

from kafka import KafkaProducer, KafkaConsumer

OBJECT_ID = random.randint(8*10**5, 9*10**5)


class CommandBus:
    
    _kafka_producer = None
    _instance = None
    _kafka_consumer = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CommandBus, cls).__new__(cls)
        return cls._instance


    def __init__(self, bootstrap_servers, **kwargs):
        self._bootstrap_servers = bootstrap_servers


    def __enter__(self):
        if not CommandBus._kafka_producer:
            CommandBus._kafka_producer = KafkaProducer(bootstrap_servers = self._bootstrap_servers)
        return self


    def __exit__(self, type, value, traceback):
        if CommandBus._kafka_producer:
            CommandBus._kafka_producer.flush()
            CommandBus._kafka_producer.close()
            CommandBus._kafka_producer = None

        if CommandBus._kafka_consumer:
            pass


    async def register_commands(self, commands_cfg):
        self._commands_cfg = commands_cfg


    async def valid(self, command):
        return True


    async def send(self, command, validate = True):
        command_ = deepcopy(command)
        uuid_ = str(uuid.uuid4())
        command_['uuid'] = uuid_

        topic_name = self._commands_cfg[command_['command_name']]['topic']
        topic_key = self._commands_cfg[command_['command_name']]['key']

        if topic_key != 'None':
            # command must be send with specialized key (keep send order in kafka)
            # TODO add dynamically object id to current topic key, e.g. "command.container.242345"
            # object id can identyfy container, stack or any object that command is related to 
            # command should contain this object id as command parameter

            # TODO make object id dynamic (from command parameters)
            topic_key += '.'+str(OBJECT_ID)

        else:
            # command not related with any object in system have no key (send to topic in round robin mode)
            topic_key = None

        CommandBus._kafka_producer.send(topic =topic_name, \
            key = bytes(topic_key, 'utf-8') if topic_key else topic_key,\
                value = bytes(json.dumps(command_), 'utf-8'))
        return uuid_


    async def consume_from(self, topic, group):
        if not CommandBus._kafka_consumer:
            CommandBus._kafka_consumer = KafkaConsumer(bootstrap_servers = self._bootstrap_servers, group_id = group)
            CommandBus._kafka_consumer.subscribe(topics = [topic])
        return CommandBus._kafka_consumer
