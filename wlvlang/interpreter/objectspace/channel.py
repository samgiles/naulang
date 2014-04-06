from wlvlang.interpreter.objectspace.object import Object

from rpython.rlib import rthread

class ChannelInterface(Object):
    def send(self, task, value):
        pass

    def receive(self, task):
        pass

class YieldException(Exception):
    pass

class SuspendException(Exception):
    pass


class BasicChannel(ChannelInterface):

    def __init__(self):
        self._queue = []

    def send(self, task, value):
        self._queue.append(value)

    def receive(self, task):
        if len(self._queue) is not 0:
            value = self._queue.pop()
            return value
        else:
            raise YieldException()

class SyncChannel(ChannelInterface):
    EMPTY = 0
    READER_WAITING = 1
    WRITER_WAITING = 2

    def __init__(self):
        self._slot = None
        self._task = None
        self._state = SyncChannel.EMPTY

    def send(self, task, value):
        self._slot = value
        if self._state is SyncChannel.EMPTY:
            self._state = SyncChannel.WRITER_WAITING
            self._task = task
            raise SuspendException()
        else:
            self._task.reschedule()

    def receive(self, task):
        if self._state is SyncChannel.EMPTY:
            self._state = SyncChannel.READER_WAITING
            self._task = task
            raise SuspendException()
        else:
            self._state = SyncChannel.EMPTY
            self._task.reschedule()
            return self._slot


