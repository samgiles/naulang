from rpythonex.rcircular import CircularArray
from rpythonex.ratomic import compare_and_swap

class CircularWorkStealingDeque(object):
    def __init__(self, log_initial_size):
        self.bottom = 0
        self.top = 0
        self.active_array = CircularArray(log_initial_size)


    def _cas_top(self, oldval, newval):
        return compare_and_swap(self.top, oldval, newval)

    def push_bottom(self, value):
        bottom = self.bottom
        top = self.top
        array = self.active_array

        size = bottom - top

        if size >= array.size() - 1:
            array = array.grow(bottom, top)
            self.active_array = array

        array.put(bottom, value)
        self.bottom = bottom + 1

    def steal(self):
        top = self.top
        bottom = self.bottom
        array = self.active_array
        size = bottom - top

        if size <= 0:
            return None

        value = array.get(top)

        if not self._cas_top(top, top + 1):
            return None

        return value

    def pop_bottom(self):
        bottom = self.bottom
        array = self.active_array
        bottom -= 1
        self.bottom = bottom
        top = self.top
        size = bottom - top
        if size < 0:
            self.bottom = top
            return None
        value = array.get(bottom)
        if size > 0:
            return value

        if not self._cas_top(top, top + 1):
            value = None

        self.bottom = top + 1
        return value
