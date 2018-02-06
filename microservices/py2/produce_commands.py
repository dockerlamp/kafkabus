import random
import uuid
from copy import deepcopy
import asyncio
import json

from systembus.commandbus import CommandBus
commands_cfg = json.load(open('systembus/commands.json'))


BOOTSTRAP_SERVERS = "172.18.0.2:9092"
CMD_RANGE = (10**6, 2*10**6)


class CommandRandomizer:

    def __init__(self, commands_cfg):
        self._commands_cfg = commands_cfg
        self._command_counter = iter(range(*CMD_RANGE))


    def rand_command(self):
        return {
            'command_name' : random.choice(list(self._commands_cfg)),
            'msg' : next(self._command_counter),
        }



async def start_produce_commands():
    cr = CommandRandomizer(commands_cfg)
    with CommandBus(bootstrap_servers = BOOTSTRAP_SERVERS) as cb:
        await cb.register_commands(commands_cfg)
        while True:
            command = cr.rand_command()
            if await cb.valid(command):
                command_uuid = await cb.send(command)
                print('command', command,'was sent, your uuid is', command_uuid)
            await asyncio.sleep(1)


loop = asyncio.get_event_loop()
loop.run_until_complete(start_produce_commands())
loop.close()
