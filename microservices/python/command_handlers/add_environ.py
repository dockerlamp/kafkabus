'''
Created on Jan 26, 2018

@author: pawel
'''

import json

from systembus.eventbus import EventBus


async def addEnvironCommandHandler(command):
    print('handling command', command)
    # TODO do stuff here...

    # emit events
    command_name = command['command_name']
    with EventBus() as eb:
        event_names = await eb.get_event_names_for(command_name)
        for event_name in event_names:
            event = {
                'event_name' : event_name,
            }
            eb.send(event)
            print('event emited', event)
