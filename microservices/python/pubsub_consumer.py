'''
Created on Jan 7, 2018

@author: pawel

kafka pub/sub scenario
'''

import json
import os
from kafka import KafkaConsumer


# kafa specific settings
TOPIC_NAME = 'example_topic'
BOOTSTRAP_SERVERS = os.environ['BOOTSTRAP_SERVERS']
AUTO_OFFSET_RESET = 'latest' # 'latest/earliest' -> default = latest



consumer = KafkaConsumer(bootstrap_servers=BOOTSTRAP_SERVERS,
                         auto_offset_reset = AUTO_OFFSET_RESET)
available_topics = consumer.topics()

#subscribe dynamically to desired topic
for topic in available_topics:
    if topic == TOPIC_NAME:
        print('found desired topic')
        consumer.subscribe(topics = [topic])
        print('subscribed to topic %s' % topic)
        
        for msg in consumer:
            encoded_value = msg.value
            decoded_value = encoded_value.decode('utf-8')
            value = json.loads(decoded_value)

            # add extra info to message
            value['partition'] = msg.partition
            value['offset'] = msg.offset
            
            print('received', value)
