'''
Created on Jan 28, 2018

@author: pawel
'''

import json

from kafka import KafkaProducer

# system settings
bus = json.load(open('../../systembus/bus.json'))
events_cfg = json.load(open('../../systembus/events.json'))

producer = KafkaProducer(bootstrap_servers = bus['bootstrap_servers'])

def emit(event_name, event):
    event_cfg = events_cfg[event_name]
    producer.send(topic= event_cfg['topic'], key = None \
                        if event_cfg['key'] == 'None' else \
                        bytes(event_cfg['key'], 'utf-8'),\
                        value = bytes(json.dumps(event), 'utf-8'))
    print('raised event', event)
    producer.flush()
