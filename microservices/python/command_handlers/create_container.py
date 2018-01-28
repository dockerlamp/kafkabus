'''
Created on Jan 26, 2018

@author: pawel
'''

import json

from kafka import KafkaProducer

# system settings
bus = json.load(open('../../systembus/bus.json'))
commands_cfg = json.load(open('../../systembus/commands.json'))
events_cfg = json.load(open('../../systembus/events.json'))
handlers_cfg = json.load(open('../../systembus/handlers.json'))

BOOTSTRAP_SERVERS = bus['bootstrap_servers']


def createContainer(command):
    print('handling command', command)
    # TODO do stuff here...

    command_name = command['command_name']
    handler_name = commands_cfg[command_name]['handler']

    # finally send events after command handled
    producer = KafkaProducer(bootstrap_servers = BOOTSTRAP_SERVERS)
    for event_name in handlers_cfg[handler_name]['event_names']:
        event_cfg = events_cfg[event_name]

        event = {
            'event_name' : event_name,
            'uuid' : command['uuid'],
            'source' : command['source'],
            }

        producer.send(topic= event_cfg['topic'], key = None \
                            if event_cfg['key'] == 'None' else \
                            bytes(event_cfg['key'], 'utf-8'),\
                            value = bytes(json.dumps(event), 'utf-8'))
        print('raised event', event)
    producer.flush()
