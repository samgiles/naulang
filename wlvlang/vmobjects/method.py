from wlvlang.vmobjects.object import Object

class Method(Object):

    def __init__(self, literals, locals, bytecodes):
        self._literals = literals
        self._locals = locals
        self._bytecodes = bytecodes

    def get_bytecode(self, index):
        assert 0 <= index and index < len(self._bytecodes)
        return self._bytecodes[index]
