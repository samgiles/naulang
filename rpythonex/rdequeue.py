from rpythonex.ratomic import compare_and_swap


class SimpleDequeue(object):
    _immutable_fields_ = ["active_array"]

    def __init__(self):
        self.active_array = []

    def push_bottom(self, value):
        self.active_array.append(value)

    def pop_bottom(self):
        if len(self.active_array) is 0:
            return None
        return self.active_array.pop()

    def steal(self):
        if len(self.active_array) is 0:
            return None
        return self.active_array.pop(0)


class CircularWorkStealingDeque(object):
    _mixin_ = True

    def __init__(self, log_initial_size):
        self.bottom = [0]
        self.top = [0]
        self.active_array = self._initialise_array(log_initial_size)

    def _initialise_array(self, log_initial_size):
        raise NotImplementedError

    def size(self):
        return self.active_array.size()

    def _cas_top(self, oldval, newval):
        return compare_and_swap(self.top, oldval, newval)

    def push_bottom(self, value):
        bottom = self.bottom[0]
        top = self.top[0]
        array = self.active_array

        size = bottom - top

        if size >= array.size() - 1:
            array = array.grow(bottom, top)
            self.active_array = array

        array.put(bottom, value)
        self.bottom[0] = bottom + 1

    def steal(self):
        top = self.top[0]
        bottom = self.bottom[0]
        array = self.active_array
        size = bottom - top

        if size <= 0:
            return None

        value = array.get(top)

        if not self._cas_top(top, top + 1):
            return None

        return value

    def pop_bottom(self):
        bottom = self.bottom[0]
        array = self.active_array
        bottom -= 1
        self.bottom[0] = bottom
        top = self.top[0]
        size = bottom - top
        if size < 0:
            self.bottom[0] = top
            return None
        value = array.get(bottom)
        if size > 0:
            return value

        if not self._cas_top(top, top + 1):
            value = None

        self.bottom[0] = top + 1
        return value
