import time
import random

from mbus import MessageBus

# test env settings
PRODUCER_ID = random.randint(10**3, 2*10**3)
MSG_NO_RANGE = (10**6, 2*10**6)
DELAY = 1

# channel
TOPIC_NAME = 'example_topic'

mbus = MessageBus()


def calculate_thoughput(timing, n_messages=1000000, msg_size=100):
    print("Processed {0} messsages in {1:.2f} seconds".format(n_messages, timing))
    print("{0:.2f} MB/s".format((msg_size * n_messages) / timing / (1024*1024)))
    print("{0:.2f} Msgs/s".format(n_messages / timing))


msg = {'producer_id': PRODUCER_ID,
    'msg_no': None,
    'topic': TOPIC_NAME}


with mbus.get_durable_channel(TOPIC_NAME) as channel:
    print('channel inited')
    start_time = time.time()
    for msg_no in range(*MSG_NO_RANGE):
        msg = {'producer_id': PRODUCER_ID,
            'msg_no': msg_no,
            'topic': TOPIC_NAME}
        channel.push(msg)
        #print('sent', msg)
        time.sleep(DELAY)


calculate_thoughput(time.time() - start_time, MSG_NO_RANGE[1] - MSG_NO_RANGE[0], len(msg))
print('all done')
