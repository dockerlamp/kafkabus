import asyncio
import json

import command_handlers
from systembus.commandbus import CommandBus
from systembus.eventbus import EventBus

commands_cfg = json.load(open('../../systembus/commands.json'))
events_cfg = json.load(open('../../systembus/events.json'))

channel = 'container_commands'


async def start_consume_commands():

    EventBus(events_config = events_cfg) # init ones
    with CommandBus(commands_config = commands_cfg) as cb:
        handlers = cb.load_handlers(command_handlers)
        for name, handler in handlers.items():
            await cb.add_handler(name, handler)

        consumer = await cb.consume_from(channel)
        for message in consumer:
            command = json.loads(message.value.decode('utf-8'))
            print('received command', command, 'channel', channel, 'key', message.key, 'partition', message.partition, 'offset', message.offset)
            # handle stuff
            command_name = command['command_name']
            handler_name = commands_cfg[command_name]['handler']
            handle = await cb.get_handler(handler_name)
            await handle(command)

            consumer.commit()

loop = asyncio.get_event_loop()
loop.run_until_complete(start_consume_commands())
loop.close()
