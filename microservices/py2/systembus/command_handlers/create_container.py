'''
Created on Jan 26, 2018

@author: pawel
'''

import json
import asyncio

from systembus.eventbus import EventBus

bus_cfg = json.load(open('systembus/bus.json'))
events_cfg = json.load(open('systembus/events.json'))

BOOTSTRAP_SERVERS = bus_cfg['bootstrap_servers']

eb = EventBus(bootstrap_servers = BOOTSTRAP_SERVERS)
eb.register_events(events_cfg)


def createContainerCommandHandler(command):
    print('handling command', command)
    # TODO do stuff here...

    # get event names to emit
    command_name = command['command_name']
    event_names = [event_name for event_name, cfg in events_cfg.items() \
                                    if command_name in cfg['on_behalf_of']]
    for event_name in event_names:
        event = {
            'event_name' : event_name,
        }
        await eb.send(event)
        print('emited event', event)
