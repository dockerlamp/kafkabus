'''
Created on Jan 18, 2018

@author: pawel
'''

import json
from kafka import KafkaConsumer, KafkaProducer

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
producer = KafkaProducer(bootstrap_servers = BOOTSTRAP_SERVERS)


#subscribe dynamically to desired topic
available_topics = consumer.topics()
for topic in available_topics:
    if topic == TOPIC_NAME:
        consumer.subscribe(topics = [topic])

        for msg in consumer:
            payload = json.loads(msg.value.decode('utf-8'))
            print('received', payload, 'key', msg.key, 'group_id', GROUP_ID, 'partition', msg.partition, 'offset', msg.offset)

            command_name = payload['command_name']
            handler_name = commands_cfg[command_name]['handler']
            # TODO create handler obj and execute it
            # emit events when handled
            for event_name in handlers_cfg[handler_name]['event_names']:
                event_cfg = events_cfg[event_name]

                event = {
                    'event_name' : event_name,
                    'uuid' : payload['uuid'],
                    'source' : payload['source'],
                    }

                producer.send(topic= event_cfg['topic'], key = None \
                                    if event_cfg['key'] == 'None' else \
                                    bytes(event_cfg['key'], 'utf-8'),\
                                    value = bytes(json.dumps(event), 'utf-8'))
                print('raised event', event)
            producer.flush()
            consumer.commit()
