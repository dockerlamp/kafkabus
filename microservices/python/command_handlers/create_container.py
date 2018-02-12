'''
Created on Jan 26, 2018

@author: pawel
'''

import json

from systembus.eventbus import EventBus

# system settings
events_cfg = json.load(open('../../systembus/events.json'))


def createContainerCommandHandler(command):
    print('handling command', command)
    # TODO do stuff here...

    # get event names to emit
    command_name = command['command_name']
    event_names = [event_name for event_name, cfg in events_cfg.items() \
                                    if command_name in cfg['on_behalf_of']]

    with EventBus(events_config = events_cfg) as eb: 
        for event_name in event_names:
            event = {
                'event_name' : event_name,
            }
            eb.send(event)
            print('event emited', event)
