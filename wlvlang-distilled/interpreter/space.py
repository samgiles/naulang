from wlvlang.vmobjects.classs import Class
from wlvlang.vmobjects.primitives.primitives import initialise_primitives
from wlvlang.vmobjects.integer import Integer
from wlvlang.vmobjects.boolean import Boolean
from wlvlang.vmobjects.string import String
from wlvlang.vmobjects.array import Array


class ObjectSpace(object):

    def __init__(self):
        self.primitive_functions = []

        # Classes define the operations that can be performed on a type
        self.integerClass = Class(self)
        self.methodClass = Class(self)
        self.booleanClass = Class(self)
        self.arrayClass = Class(self)
        self.primitiveClass = Class(self)
        self.stringClass = Class(self)

        self.initialise_primitives()

    def initialise_primitives(self):
        # Initialise prims
        initialise_primitives(self)

    def get_primitive_function(self, index):
        return self.primitive_functions[index]

    def add_primitive_function(self, index, function):
        self.primitive_functions[index] = function

    def new_integer(self, value):
        return Integer(value)

    def new_boolean(self, value):
        return Boolean(value)

    def new_array(self, initial_size):
        return Array(initial_size)

    def new_string(self, value):
        return String(value)
