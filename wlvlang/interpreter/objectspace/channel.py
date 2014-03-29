from wlvlang.interpreter.objectspace.object import Object

from rpython.rlib import rthread

class ChannelInterface(Object):
    def send(self, value):
        pass

    def receive(self):
        pass

class YieldException(Exception):
    pass


class BasicChannel(ChannelInterface):

    def __init__(self):
        self._queue = []

    def send(self, value):
        self._queue.append(value)

    def receive(self):
        if len(self._queue) is not 0:
            value = self._queue.pop()
            return value
        else:
            raise YieldException()
