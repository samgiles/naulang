from wlvlang.interpreter.objectspace.klass import Class
from wlvlang.interpreter.objectspace.integer import Integer
from wlvlang.interpreter.objectspace.boolean import Boolean
from wlvlang.interpreter.objectspace.string import String
from wlvlang.interpreter.objectspace.array import Array
from wlvlang.interpreter.objectspace.channel import BasicChannel

from wlvlang.interpreter.objectspace.primitives.primitives import initialise_primitives

from rpython.rlib import jit


class ObjectSpace(object):

    _immutable_fields_ = ["builtin_functions[*]"]

    def __init__(self):
        # Classes define the operations that can be performed on a type
        self.integerClass = Class()
        self.methodClass = Class()
        self.booleanClass = Class()
        self.arrayClass = Class()
        self.builtinClass = Class()
        self.stringClass = Class()

        self.builtin_functions = []
        self.initialise_primitives()

    def initialise_primitives(self):
        # Initialise prims
        initialise_primitives(self)

    def get_builtin_function(self, index):
        return self.builtin_functions[index]

    def add_builtin_function(self, index, function):
        self.builtin_functions[index] = function

    @jit.elidable
    def new_integer(self, value):
        jit.promote(value)
        return Integer(value)

    @jit.elidable
    def new_boolean(self, value):
        jit.promote(value)
        return Boolean(value)

    @jit.elidable
    def new_array(self, initial_size):
        jit.promote(initial_size)
        return Array(initial_size)

    @jit.elidable
    def new_string(self, value):
        jit.promote(value)
        return String(value)

    def new_channel(self):
        return BasicChannel()
