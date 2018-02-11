from abc import ABC, abstractmethod


class IBus(ABC):

    @abstractmethod
    async def send(self, message):
        pass


    @abstractmethod
    async def consume_from(self, topic, group):
        pass


    @abstractmethod
    async def add_handler(self, name, handler):
        pass

