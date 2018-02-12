import json

from .ibus import IBus
from .kafkabus import KafkaBus

# platform settings
bus_config = json.load(open('../../systembus/bus.json'))


class EventBus(IBus, KafkaBus):
    '''singleton'''
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(EventBus, cls).__new__(cls)
        return cls._instance


    def __init__(self, events_config = None):
        super().__init__(bus_config)
        if events_config:
            self.events_config = events_config

        if not hasattr(self, 'event_handlers'):
            self.event_handlers = {}


    async def add_handler(self, name, event_handler):
        if name in self.event_handlers:
            raise ValueError('Event handler %s already registered!')
        self.event_handlers[name] = event_handler


    async def send(self, event):
        topic_name = self.events_config[event['event_name']]['topic']
        topic_key = self.events_config[event['event_name']]['key']
        topic_key = None if topic_key == 'None' else topic_key 

        self.__enter__() # ensure kafka producer is ready
        self._producer.send(topic = topic_name, key = bytes(topic_key, 'utf-8') if topic_key else topic_key,\
            value = bytes(json.dumps(event), 'utf-8'))
        return


    async def consume_from(self, topic, group):
        # TODO use "channels" attrib from bus.json instead of topic and group?
        return await self._get_consumer(topic, group)


    async def get_handler(self, name):
        return self.event_handlers[name]


    async def get_event_names_for(self, command_name):
        return [event_name for event_name, cfg in self.events_config.items() \
                                    if command_name in cfg['on_behalf_of']]
