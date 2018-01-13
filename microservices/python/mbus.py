import os
import json

from confluent_kafka import Producer, Consumer, KafkaException


# kafka settings
KAFKA_CONFIG = {
    'bootstrap.servers' : os.environ['BOOTSTRAP_SERVERS'],
    }


class _BaseChannel():
    '''
    '''
    _shared_producer = None
    _shared_consumer = None



class Channel(_BaseChannel):
    
    def __init__(self, name):
        '''
        '''
        self.name = name


    def __enter__(self):
        return self
    
    
    def __exit__(self, exc_type, exc_value, traceback):
        if _BaseChannel._shared_producer:
            _BaseChannel._shared_producer.flush()


    def __repr__(self):
        '''
        '''
        return '%s(name=%s)' % (self.__class__.__name__, self.name)


    def push(self, message):
        '''
        '''
        if not _BaseChannel._shared_producer:
            _BaseChannel._shared_producer = Producer(KAFKA_CONFIG)
        _BaseChannel._shared_producer.produce(self.name, value = json.dumps(message).encode('utf-8'))


class DurableChannel(_BaseChannel):
    
    def __init__(self, name, ):
        '''
        '''
        self.name = name


    def __enter__(self):
        return self
    
    
    def __exit__(self, exc_type, exc_value, traceback):
        if _BaseChannel._shared_producer:
            _BaseChannel._shared_producer.flush()


    def __repr__(self):
        '''
        '''
        return '%s(name=%s)' % (self.__class__.__name__, self.name)


    def push(self, message):
        '''
        '''

        if not _BaseChannel._shared_producer:
            _BaseChannel._shared_producer = Producer(KAFKA_CONFIG)
            if not _BaseChannel._shared_producer: print('shit happens')
        #_BaseChannel._shared_producer.produce(self.name, value = json.dumps(message).encode('utf-8'))





class MessageBus():

    def __init__(self):
        pass
    
    def get_channel(self, name):
        return Channel(name)

    def get_durable_channel(self, name):
        return DurableChannel(name)
