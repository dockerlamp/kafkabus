'''
Created on Jan 9, 2018

@author: pawel
'''

import random
import json
import time

from message_bus import MessageBus


# test env settings
PRODUCER_ID = random.randint(10**3, 2*10**3)
MSG_NO_RANGE = (10**6, 2*10**6)
DELAY = 1

# kafka settings
TOPIC_NAME = 'example_topic'


mbus = MessageBus()
with mbus.get_durable_channel(TOPIC_NAME) as channel:

    for msg_no in range(*MSG_NO_RANGE):
        msg = {'producer_id': PRODUCER_ID,
                'msg_no': msg_no,
                'topic_name': TOPIC_NAME}

        result = channel.push(bytes(json.dumps(msg), 'utf-8'), flush = False)
        #print('sent ', msg)
        time.sleep(DELAY)
