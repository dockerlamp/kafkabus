'''
Created on Jan 7, 2018

@author: pawel
'''

import time
import random
import json
import os


from kafka import KafkaProducer

# test env settings
PRODUCER_ID = random.randint(10**3, 2*10**3)
MSG_NO_RANGE = (10**6, 2*10**6)
DELAY = 2

# kafa specific settings
TOPIC_NAME = 'pubsub_topic'
BOOTSTRAP_SERVERS = os.environ['BOOTSTRAP_SERVERS']

'''
..Note::
    If no topic in kafka, producer will open topic with default settings (one
    partition, random partition assignment).
'''



msg_pattern = {'producer_id' : None, 
                'msg_no' : None,
                'topic_name' : None}


producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)

for msg_no in range(*MSG_NO_RANGE):
    
    msg = dict(msg_pattern)
    msg['producer_id'] = PRODUCER_ID
    msg['msg_no'] = msg_no
    msg['topic_name'] = TOPIC_NAME

    producer.send(topic =TOPIC_NAME, value = bytes(json.dumps(msg), 'utf-8'))
    producer.flush()
    print('sent ', msg)
    time.sleep(DELAY)
