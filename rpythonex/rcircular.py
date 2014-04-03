from rpython.rlib import jit
class CircularArray(object):
    """ Simple Circular Array implementation based on implementation by Chase and Lev (2005)  http://dx.doi.org/10.1145/1073970.1073974
    """

    _immutable_ = True
    _immutable_fields_ = ["_segment", "_logarithmic_size"]
    def __init__(self, logarithmic_size, initial_value=None):
        self._logarithmic_size = logarithmic_size
        self._segment = [initial_value] * (0x01 << self._logarithmic_size)

    @jit.elidable
    def size(self):
        return 1 << self._logarithmic_size

    def get(self, index):
        return self._segment[index % self.size()]

    def put(self, index, obj):
        self._segment[index % self.size()] = obj

    @jit.unroll_safe
    def grow(self, bottom, top):
        new_circular = CircularArray(self._logarithmic_size + 1)
        index = top
        while index < bottom:
            new_circular.put(index, self.get(index))
            index += 1

        return new_circular
