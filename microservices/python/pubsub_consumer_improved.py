'''
Created on Jan 7, 2018

@author: pawel

kafka pub/sub scenario
'''

import json
from kafka_bus import message_bus

# kafka specific settings
topic_name = 'pubsub_topic'
extra_settings = {
    #'auto_offset_reset' = 'latest', # 'latest/earliest' -> default = latest
}

channel = message_bus.consume_from(topic_name, **extra_settings)

for msg in channel:
    encoded_value = msg.value
    decoded_value = encoded_value.decode('utf-8')
    value = json.loads(decoded_value)

    # add extra info to message
    value['partition'] = msg.partition
    value['offset'] = msg.offset

    print('received', value)
