from wlvlang.interpreter.objectspace.klass import Class
from wlvlang.interpreter.objectspace.integer import Integer
from wlvlang.interpreter.objectspace.boolean import Boolean
from wlvlang.interpreter.objectspace.string import String
from wlvlang.interpreter.objectspace.array import Array

from wlvlang.interpreter.objectspace.primitives.primitives import initialise_primitives


class ObjectSpace(object):

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
        return self.builitin_function[index]

    def add_builtin_function(self, index, function):
        self.builtin_functions[index] = function

    def new_integer(self, value):
        return Integer(value)

    def new_boolean(self, value):
        return Boolean(value)

    def new_array(self, initial_size):
        return Array(initial_size)

    def new_string(self, value):
        return String(value)
