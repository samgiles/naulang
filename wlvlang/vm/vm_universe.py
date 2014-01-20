from wlvlang.vmobjects.classs import Class
from wlvlang.vmobjects.primitives.primitives import initialise_primitives
from wlvlang.vmobjects.integer import Integer

from wlvlang.vm.symbol_table import SymbolTable


class VM_Universe(object):

    def __init__(self):
        self._symbol_table = SymbolTable()
        self.integerClass = None
        self.initialise_primitives()

    def initialise_primitives(self):
        self.integerClass = Class(self)

        # Initialise prims
        initialise_primitives(self)

    def new_integer(self, value):
        return Integer(value)

    def symbol_for(self, string):
        symbol = self._symbol_table.get(string, None)

        if symbol:
            return symbol

        new_symbol = Symbol(string)
        self._symbol_table.insert(new_symbol)
        return new_symbol
