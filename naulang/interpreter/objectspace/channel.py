from naulang.interpreter.objectspace.object import Object

from rpythonex.rdequeue import CircularWorkStealingDeque
from rpythonex.rcircular import CircularArray

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
    def __init__(self):
        self._slot = None
        self._task = None

    def send(self, task, value):
        # if the channel is empty
        if self._task is None:
            self._task = task
            self._slot = value
            raise SuspendException

        # A reader is waiting:
        # store the value in the slot
        self._slot = value
        # reschedule the reader
        self._task.reschedule()
        # Store a reference to this task, the reader will reschedule it
        # once it has read the value
        self._task = task
        raise SuspendException

    def receive(self, task):
        if self._task is None:
            # READER WAITING
            self._task = task
            raise SuspendException

        # if sender waiting
        value = self._slot
        self._task.reschedule()
        self._task = None
        return value

class ChannelCircularArray(CircularArray):
    def _create_new_instance(self, new_size):
        return ChannelCircularArray(new_size)

class ChannelDequeue(CircularWorkStealingDeque):
    def _initialise_array(self, log_initial_size):
        return ChannelCircularArray(log_initial_size)

class DequeueChannel(ChannelInterface):
    def __init__(self):
        self._queue = ChannelDequeue(1)

    def send(self, task, value):
        self._queue.push_bottom(value)

    def receive(self, task):
        value = self._queue.steal()
        if value is None: raise YieldException()
        return value
