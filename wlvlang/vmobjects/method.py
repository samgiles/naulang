from wlvlang.vmobjects.object import Object
from rpython.rlib import jit

class Method(Object):

    _immutable_fields_ = ['_bytecodes']

    def __init__(self, literals, locals, bytecodes):
        self._literals = literals
        self._locals = locals
        self._bytecodes = bytecodes

    @jit.elidable
    def get_bytecode(self, index):
        assert 0 <= index and index < len(self._bytecodes)
        return self._bytecodes[index]
