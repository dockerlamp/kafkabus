import pickle
import random
import time
import os

from kafka import KafkaProducer

KAFKA_TOPIC_NAME = os.environ['KAFKA_TOPIC_NAME']
BOOTSTRAP_SERVERS = os.environ['BOOTSTRAP_SERVERS']
MSG_SENT_FREQUENCY = 1

if __name__ == '__main__':
    info_txt = 'producer settings: topic is %s, bootstrap srv is %s' % (KAFKA_TOPIC_NAME, BOOTSTRAP_SERVERS)
    print(info_txt)

    producer = KafkaProducer(bootstrap_servers = BOOTSTRAP_SERVERS,
                                acks = 'all',
                                value_serializer = pickle.dumps)

    def random_message_generator():
        while True:
            yield 'random message tadeusz no. %d' % random.randint(1, 10**6)
            time.sleep(MSG_SENT_FREQUENCY)

    for msg in random_message_generator():
        producer.send(KAFKA_TOPIC_NAME, value=msg)
        #print('known partitions: %s' % producer.partitions_for(KAFKA_TOPIC_NAME))
        print('sent %s' % msg)
        producer.flush()
	


# comment
