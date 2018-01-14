'''
Created on Jan 7, 2018

@author: pawel

kafka pub/sub scenario
'''

import random
import json

from message_bus import MessageBus

# test env settings
CONSUMER_ID = random.randint(3*10**3, 4*10**3)

# kafka consumer settings
TOPIC_NAME = 'example_topic'


mbus = MessageBus()
channel = mbus.get_durable_channel(TOPIC_NAME).pull()

for msg in channel:
    encoded_value = msg.value
    decoded_value = encoded_value.decode('utf-8')
    value = json.loads(decoded_value)
    
    # add extra info to message
    value['consumer_id'] = CONSUMER_ID
    value['partition'] = msg.partition
    value['offset'] = msg.offset

    channel.commit()
    print('received', value)

