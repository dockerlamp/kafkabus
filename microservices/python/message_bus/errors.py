'''
Created on Jan 9, 2018

@author: pawel
'''

class MessageBusError(Exception):
    pass

class ChannelNotFoundError(MessageBusError):
    pass

class MessageNotSendError(MessageBusError):
    pass
