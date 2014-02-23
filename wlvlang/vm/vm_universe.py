from wlvlang.vmobjects.classs import Class
from wlvlang.vmobjects.primitives.primitives import initialise_primitives
from wlvlang.vmobjects.integer import Integer
from wlvlang.vmobjects.boolean import Boolean
from wlvlang.vmobjects.string import String
from wlvlang.vmobjects.array import Array

from wlvlang.vm.symbol_table import SymbolTable

from rpython.rlib import jit


class VM_Universe(object):

    def __init__(self):
        self.primitive_functions = []
        self._symbol_table = SymbolTable()
        self.integerClass = None
        self.methodClass = None
        self.booleanClass = None
        self.arrayClass = None
        self.primitiveClass = None
        self.stringClass = None
        self.initialise_primitives()

    def initialise_primitives(self):
        self.integerClass = Class(self)
        self.methodClass = Class(self)
        self.booleanClass = Class(self)
        self.arrayClass = Class(self)
        self.primitiveClass = Class(self)
        self.stringClass = Class(self)

        # Initialise prims
        initialise_primitives(self)

    def get_primitive_function(self, index):
        return self.primitive_functions[index]

    def add_primitive_function(self, index, function):
        self.primitive_functions[index] = function


    @jit.elidable
    def new_integer(self, value):
        return Integer(value)

    @jit.elidable
    def new_boolean(self, value):
        return Boolean(value)

    @jit.elidable
    def new_array(self, initial_size):
        return Array(initial_size)

    @jit.elidable
    def new_string(self, value):
        return String(value)
