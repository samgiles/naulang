from rpython.rlib import jit

class Symbol(object):

    _immutable_fields_ = ["_string", "_arguments", "_argument_count"]

    def __init__(self, value):
        self._string = value
        self._arguments = self._get_arguments_as_list()
        self._argument_count = len(self._arguments)

    def _get_arguments_as_list(self):
        parts = []

        current = ""

        for c in self._string:
            if c == '.':
                parts.append(current)
                current = ""
            else:
                current = current + c

        parts.append(current)

        return parts

    @jit.elidable
    def get_string(self):
        return self._string
