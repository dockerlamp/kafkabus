'''
Created on Jan 26, 2018

@author: pawel
'''

import json

from kafka import KafkaProducer

import event_producer

# system settings
commands_cfg = json.load(open('../../systembus/commands.json'))
handlers_cfg = json.load(open('../../systembus/handlers.json'))


def addEnviron(command):
    print('handling command', command)
    # TODO do stuff here...

    command_name = command['command_name']
    handler_name = commands_cfg[command_name]['handler']

    # finally send events after command handled
    for event_name in handlers_cfg[handler_name]['event_names']:

        event = {
            'event_name' : event_name,
            'uuid' : command['uuid'],
            'source' : command['source'],
            }
        event_producer.emit(event_name, event)
