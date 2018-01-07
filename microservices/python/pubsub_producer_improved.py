'''
Created on Jan 7, 2018

@author: pawel
kafka pub/sub scenario
'''

import time
import random
import json

from kafka_bus import message_bus

# test env settings
PRODUCER_ID = random.randint(10**3, 2*10**3)
MSG_NO_RANGE = (10**6, 2*10**6)
DELAY = 2
# kafa specific settings
topic_name = 'pubsub_topic'
extra_settings = {}

channel = message_bus.produce_to(**extra_settings)

for msg_no in range(*MSG_NO_RANGE):
    msg = {'producer_id':PRODUCER_ID, 'msg_no':msg_no, 'topic_name':topic_name}

    channel.send(topic_name, value = bytes(json.dumps(msg), 'utf-8'))
    channel.flush()
    print('sent ', msg)
    time.sleep(DELAY)
