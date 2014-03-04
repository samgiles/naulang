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
        self._lock = rthread.allocate_lock()
        self._queue = []

    def send(self, value):
        with self._lock:
            self._queue.append(value)

    def receive(self):
        with self._lock:
            if len(self._queue) is not 0:
                return self._queue.pop()
            else:
                raise YieldException()
