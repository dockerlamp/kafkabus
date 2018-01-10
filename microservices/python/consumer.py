'''
Created on Jan 7, 2018

@author: pawel

kafka pub/sub scenario
'''

import random
import json
import asyncio

import message_bus

# test env settings
CONSUMER_ID = random.randint(3*10**3, 4*10**3)


# kafka consumer settings
TOPIC_NAME = 'example_topic'
KAFKA_CONFIG = {
    'auto_offset_reset': 'earliest', # resume from last commit, default 'latest'
    'group_id': 'example_group,' # use groups for durable queue
}


async def consume():
    channel = await message_bus.output_channel(TOPIC_NAME, KAFKA_CONFIG)

    for msg in channel:
        encoded_value = msg.value
        decoded_value = encoded_value.decode('utf-8')
        value = json.loads(decoded_value)
    
        # add extra info to message
        value['consumer_id'] = CONSUMER_ID
        value['partition'] = msg.partition
        value['offset'] = msg.offset

        channel.commit()
        print('received', value, 'config', KAFKA_CONFIG)

loop = asyncio.get_event_loop()
loop.run_until_complete(consume())
loop.close()
