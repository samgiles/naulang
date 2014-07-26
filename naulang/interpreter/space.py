from naulang.interpreter.objectspace.integer import Integer
from naulang.interpreter.objectspace.float import Float
from naulang.interpreter.objectspace.boolean import Boolean
from naulang.interpreter.objectspace.string import String
from naulang.interpreter.objectspace.array import Array
from naulang.interpreter.objectspace.channel import BasicChannel, SyncChannel

from naulang.interpreter.objectspace.primitives.primitives import initialise_primitives


class ObjectSpace(object):

    _immutable_fields_ = [
        "builtin_functions[*]",
    ]

    def __init__(self):
        self.builtin_functions = []
        self.initialise_primitives()

    def initialise_primitives(self):
        initialise_primitives(self)

    def get_builtin_function(self, index):
        return self.builtin_functions[index]

    def add_builtin_function(self, index, function):
        self.builtin_functions[index] = function

    def new_integer(self, value):
        return Integer(int(value))

    def new_float(self, value):
        return Float(float(value))

    def new_boolean(self, value):
        return Boolean(value)

    def new_array(self, initial_size):
        return Array(initial_size)

    def new_string(self, value):
        return String(value)

    def new_channel(self):
        return SyncChannel()

    def new_asyncchannel(self):
        return BasicChannel()
