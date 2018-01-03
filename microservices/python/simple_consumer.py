import pickle
import random
import time
import os

from kafka import KafkaConsumer

KAFKA_TOPIC_NAME = os.environ['KAFKA_TOPIC_NAME']
BOOTSTRAP_SERVERS = os.environ['BOOTSTRAP_SERVERS']

if __name__ == '__main__':
    info_txt = 'consumer settings: topic is %s, bootstrap srv is %s' % (KAFKA_TOPIC_NAME, BOOTSTRAP_SERVERS)
    print(info_txt)

    consumer = KafkaConsumer(KAFKA_TOPIC_NAME, bootstrap_servers= BOOTSTRAP_SERVERS, value_deserializer = pickle.loads)
    for msg in consumer:
        print ('recived %s from topic=%s, partition=%d, key=%s' % (msg.value, msg.topic, msg.partition, msg.key))
