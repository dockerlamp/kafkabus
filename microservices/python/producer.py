'''
Created on Jan 18, 2018

@author: pawel
'''

import time
import random
import json

from kafka import KafkaProducer

bus = json.load(open('../../systembus/bus.json'))
commands_cfg = json.load(open('../../systembus/commands.json'))


# test env settings
COMMAND_NAME = random.choice(list(commands_cfg))
COMMAND_CFG = commands_cfg[COMMAND_NAME]
OBJ_ID = random.randint(8*10**4, 9*10**4)
PRODUCER_ID = random.randint(10**3, 2*10**3)
MSG_NO_RANGE = (10**6, 2*10**6)
DELAY = 3


# kafka settings
BOOTSTRAP_SERVERS = bus['bootstrap_servers']
TOPIC_NAME = COMMAND_CFG['topic']
KEY = None if COMMAND_CFG['key'] == 'None' else COMMAND_CFG['key']+'.'+str(OBJ_ID)


producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)

for msg_no in range(*MSG_NO_RANGE):

    msg = {
        'uuid' : random.randint(5*10**5, 6*10**5),
        'source' : PRODUCER_ID,
        'msg' : msg_no,
        'command_name' : COMMAND_NAME,
        }

    producer.send(topic =TOPIC_NAME, key = bytes(KEY, 'utf-8') if KEY else KEY,\
                                    value = bytes(json.dumps(msg), 'utf-8'))
    #print('sent', msg)
    time.sleep(DELAY)
producer.flush()
