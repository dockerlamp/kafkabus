'''
Created on Jan 18, 2018

@author: pawel
'''

import json
from kafka import KafkaConsumer

import command_handlers
from handlers import register


# system settings
bus = json.load(open('../../systembus/bus.json'))
commands_cfg = json.load(open('../../systembus/commands.json'))
events_cfg = json.load(open('../../systembus/events.json'))
handlers_cfg = json.load(open('../../systembus/handlers.json'))


# kafa consumer specific settings
TOPIC_NAME = bus['channels']['container_commands']['topic']
BOOTSTRAP_SERVERS = bus['bootstrap_servers']
AUTO_OFFSET_RESET = bus['channels']['container_commands']['auto_offset_reset']
GROUP_ID = bus['channels']['container_commands']['group_id']


consumer = KafkaConsumer(bootstrap_servers = BOOTSTRAP_SERVERS,
                         auto_offset_reset = AUTO_OFFSET_RESET,
                         group_id = GROUP_ID)
command_handlers_registry = register(command_handlers)


#subscribe dynamically to desired topic
available_topics = consumer.topics()
for topic in available_topics:
    if topic == TOPIC_NAME:
        consumer.subscribe(topics = [topic])

        for msg in consumer:
            command = json.loads(msg.value.decode('utf-8'))
            print('received command', 'key', msg.key, 'group_id', GROUP_ID, 'partition', msg.partition, 'offset', msg.offset)
            command_name = command['command_name']
            handler_name = commands_cfg[command_name]['handler']
            # handle command
            handler = command_handlers_registry[handler_name]
            handler(command)
            consumer.commit()
