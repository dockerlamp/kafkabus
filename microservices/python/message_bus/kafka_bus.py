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
KAFKA_PRODUCER_CONFIG = {
    #'request_timeout_ms' : 3000, # must be >= broker session timeout
    }
KAFKA_CONSUMER_CONFIG = {
    'auto_offset_reset': 'earliest', # resume from last commit, default 'latest'
    'group_id': 'example_group,' # use groups for durable queue
}


# message bus settings
MAX_RETRY = 100
RETRY_INTERVAL_MS = 1000


class _BaseChannel():
    '''
    '''
    _shared_producer = None
    _shared_consumer = None


class DurableChannel(_BaseChannel):

    def __init__(self, name):
        '''
        '''
        self.name = name


    @retry(msg = 'Connecting to channel', max_retry= MAX_RETRY, interval_ms = RETRY_INTERVAL_MS)
    def __enter__(self):
        '''
        '''

        if not _BaseChannel._shared_producer:
            _BaseChannel._shared_producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS, **KAFKA_PRODUCER_CONFIG)

        if not _BaseChannel._shared_consumer:
            _BaseChannel._shared_consumer = KafkaConsumer(bootstrap_servers=BOOTSTRAP_SERVERS, **KAFKA_CONSUMER_CONFIG)     

        return self


    def __exit__(self, exc_type, exc_value, traceback):
        if _BaseChannel._shared_producer:
            _BaseChannel._shared_producer.flush()


    def __repr__(self):
        '''
        '''
        return '%s(name=%s)' % (self.__class__.__name__, self.name)


    @retry(msg = 'Pushing to channel', max_retry= MAX_RETRY, interval_ms = RETRY_INTERVAL_MS)
    def push(self, message, flush = False):
        '''
        '''
        future = _BaseChannel._shared_producer.send(topic= self.name, value= message)
        future.get() # get sent record or exception on failure

        if flush: _BaseChannel._shared_producer.flush()


    @retry(msg = 'Connecting to channel', max_retry= MAX_RETRY, interval_ms = RETRY_INTERVAL_MS)
    def pull(self):
        '''
        '''
        if not _BaseChannel._shared_consumer:
            _BaseChannel._shared_consumer = KafkaConsumer(bootstrap_servers=BOOTSTRAP_SERVERS, **KAFKA_CONSUMER_CONFIG)
        
        available_topics = _BaseChannel._shared_consumer.topics()
        if self.name not in available_topics:
            raise errors.ChannelNotFoundError(self.name+' not found')
        _BaseChannel._shared_consumer.subscribe(topics = [self.name])

        return _BaseChannel._shared_consumer


class MessageBus():
    
    def __init__(self):
        pass


    def get_durable_channel(self, name):
        return DurableChannel(name)
