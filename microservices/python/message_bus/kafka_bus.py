'''
Created on Jan 8, 2018

@author: pawel
'''

import os

from kafka import KafkaProducer, KafkaConsumer

from message_bus.misc import retry
from message_bus import errors

# kafka settings
BOOTSTRAP_SERVERS = os.environ['BOOTSTRAP_SERVERS']

# message bus settings
MAX_RETRY = 100
RETRY_INTERVAL_MS = 1000


@retry(msg = 'Getting input channel', max_retry= MAX_RETRY, interval_ms = 
                                                            RETRY_INTERVAL_MS)
def input_channel(config):
    return  KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS, **config)




@retry(msg = 'Getting output channel', max_retry= MAX_RETRY, interval_ms = 
                                                            RETRY_INTERVAL_MS)
def output_channel(topic, config):
    consumer = KafkaConsumer(bootstrap_servers=BOOTSTRAP_SERVERS, **config)
    
    available_topics = consumer.topics()
    if topic not in available_topics:
        raise errors.ChannelNotFoundError(topic)
    consumer.subscribe(topics = [topic])
    return consumer
