from wlvlang.vmobjects.classs import Class
from wlvlang.vmobjects.primitives.primitives import initialise_primitives
from wlvlang.vmobjects.integer import Integer
from wlvlang.vmobjects.boolean import Boolean

from wlvlang.vm.symbol_table import SymbolTable

from rpython.rlib import jit


class VM_Universe(object):

    def __init__(self):
        self._symbol_table = SymbolTable()
        self.integerClass = None
        self.methodClass = None
        self.booleanClass = None
        self.arrayClass = None
        self.initialise_primitives()

    def initialise_primitives(self):
        self.integerClass = Class(self)
        self.methodClass = Class(self)
        self.booleanClass = Class(self)
        self.arrayClass = Class(self)

        # Initialise prims
        initialise_primitives(self)

    @jit.elidable
    def new_integer(self, value):
        return Integer(value)

    @jit.elidable
    def new_boolean(self, value):
        return Boolean(value)

