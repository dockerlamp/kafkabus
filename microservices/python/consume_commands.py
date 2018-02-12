import asyncio
import json

import command_handlers
from systembus.commandbus import CommandBus

commands_cfg = json.load(open('../../systembus/commands.json'))

TOPIC = 'container_commands'
GROUP = 'alfa'


async def start_consume_commands():

    with CommandBus(commands_config = commands_cfg) as cb:

        handlers = cb.load_handlers(command_handlers)
        for name, handler in handlers.items():
            await cb.add_handler(name, handler)

        consumer = await cb.consume_from(topic = TOPIC, group = GROUP)
        for message in consumer:
            command = json.loads(message.value.decode('utf-8'))
            print('received command', command, 'key', message.key, 'group_id', GROUP, 'partition', message.partition, 'offset', message.offset)
            # handle stuff
            command_name = command['command_name']
            handler_name = commands_cfg[command_name]['handler']
            handle = await cb.get_handler(handler_name)
            handle(command)

            consumer.commit()

loop = asyncio.get_event_loop()
loop.run_until_complete(start_consume_commands())
loop.close()
