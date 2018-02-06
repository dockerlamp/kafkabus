'''
Created on Jan 26, 2018

@author: pawel
'''

import json

events_cfg = json.load(open('systembus/events.json'))


def addVolumeToContainerCommandHandler(command):
    print('handling command', command)
    # TODO do stuff here...

    # get event names to emit
    command_name = command['command_name']
    event_names = [event_name for event_name, cfg in events_cfg.items() \
                                    if command_name in cfg['on_behalf_of']]
    for event_name in event_names:
        # TODO emit event
        pass
