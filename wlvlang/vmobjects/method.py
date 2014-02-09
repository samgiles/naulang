from wlvlang.vmobjects.object import Object
from rpython.rlib import jit

class Method(Object):

    _immutable_fields_ = ['_bytecodes', '_literals', '_signature']

    def __init__(self, signature, literals, locals, bytecodes):
        self._literals = literals
        self._locals = locals
        self._bytecodes = bytecodes
        self._signature

    @jit.elidable
    def get_bytecode(self, index):
        assert 0 <= index and index < len(self._bytecodes)
        return self._bytecodes[index]

    @jit.elidable
    def get_literals(self):
        return self._literals

    @jit.elidable
    def get_signature(self):
        return self._signature
