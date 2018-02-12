import json
import asyncio
from sys import path

path.append('../')

import event_handlers
import command_handlers
from .commandbus import CommandBus
from .eventbus import EventBus

# platform settings
commands_config = json.load(open('../../systembus/commands.json'))
events_config = json.load(open('../../systembus/events.json'))


with CommandBus(commands_config) as cb1, CommandBus() as cb2, EventBus(events_config) as eb:
    print(cb1, cb2)
    print(id(cb1.bus_config), id(cb2.bus_config))

    chandlers = cb1.load_handlers(command_handlers)
    print(chandlers)

    for name, handler in chandlers.items():
        cb1.add_handler(name, handler)

    print(id(cb1.command_handlers), id(cb2.command_handlers))

    ehandlers = eb.load_handlers(event_handlers)
    print(ehandlers)

    for name, handler in ehandlers.items():
        eb.add_handler(name, handler) 
