import json
import asyncio
from sys import path

path.append('../')

import event_handlers
from commandbus import CommandBus

# platform settings
commands_config = json.load(open('../../../systembus/commands.json'))


with CommandBus(commands_config) as cb1, CommandBus() as cb2:
    print(cb1, cb2)
    print(id(cb1.bus_config), id(cb2.bus_config))

    handlers = cb1.load_handlers(event_handlers)
    print(handlers)

    for name, handler in handlers.items():
        cb1.add_handler(name, handler)

    print(id(cb1.command_handlers), id(cb2.command_handlers))
