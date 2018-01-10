'''
Created on Jan 9, 2018

@author: pawel
'''

import random
import json
import asyncio

import message_bus


# test env settings
PRODUCER_ID = random.randint(10**3, 2*10**3)
MSG_NO_RANGE = (10**6, 2*10**6)
DELAY = 0.5


# kafka settings
TOPIC_NAME = 'example_topic'
KAFKA_CONFIG = {
    'request_timeout_ms' : 3000, # when re send on error
    }


async def produce():
    channel = await message_bus.input_channel(KAFKA_CONFIG)

    for msg_no in range(*MSG_NO_RANGE):
        msg = {'producer_id': PRODUCER_ID,
               'msg_no': msg_no,
               'topic_name': TOPIC_NAME}

        future = channel.send(topic= TOPIC_NAME, value= 
                                            bytes(json.dumps(msg), 'utf-8'))
        channel.flush()
        if future.failed():
            raise message_bus.errors.MessageNotSendError(
                                'topic: %s, message:%s'% (TOPIC_NAME, msg))
        print('sent ', msg, 'config', KAFKA_CONFIG)
        await asyncio.sleep(DELAY)

loop = asyncio.get_event_loop()
loop.run_until_complete(produce())
loop.close()
