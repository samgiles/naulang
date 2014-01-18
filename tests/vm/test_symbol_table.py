import pytest

from wlvlang.vm.symbol_table import SymbolTable
from wlvlang.vmobjects.symbol import Symbol

def test_insert_and_lookup():
    subject = SymbolTable()

    subject.insert(Symbol("hello.world"))
    symbol = subject.lookup("hello.world")

    assert(symbol.get_string() == "hello.world")
