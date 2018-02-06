import random
import uuid
from copy import deepcopy
import asyncio
import json

from systembus.commandbus import CommandBus

bus_cfg = json.load(open('systembus/bus.json'))
commands_cfg = json.load(open('systembus/commands.json'))

BOOTSTRAP_SERVERS = bus_cfg['bootstrap_servers']
TOPIC = bus_cfg['topics']['container_commands']['topic']
GROUP = bus_cfg['topics']['container_commands']['group_id']


async def start_consume_commands():
    with CommandBus(bootstrap_servers = BOOTSTRAP_SERVERS) as cb:
        await cb.register_commands(commands_cfg)
        consumer = await cb.consume_from(topic = TOPIC, group = GROUP)
        for message in consumer:
            command = json.loads(message.value.decode('utf-8'))
            print('received command', command, 'key', message.key, 'group_id', GROUP, 'partition', message.partition, 'offset', message.offset)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_consume_commands())
loop.close()
