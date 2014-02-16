from wlvlang.vmobjects.object import Object
from wlvlang.compiler.disassembler import Disassembler

from wlvlang.interpreter.activationrecord import ActivationRecord
from rpython.rlib import jit

class Method(Object):
    """ Defines a Method in the wlvlang-vm. """

    _immutable_fields_ = ['_bytecodes', '_signature']

    def __init__(self, signature, literals, locals, bytecodes, argument_count=0):
        self._literals = literals
        self._locals = locals
        self._bytecodes = bytecodes
        self._signature = signature
        self._argument_count = argument_count

    def get_bytecode(self, index):
        assert 0 <= index and index < len(self._bytecodes)
        return self._bytecodes[index]

    def get_literals(self):
        return self._literals

    def get_signature(self):
        return self._signature

    def invoke(self, activation_record, interpreter, parent=None):
        new_arec = ActivationRecord(self._locals + self._literals, len(self._locals), len(self._literals), 200, activation_record, access_link=parent)

        # Push arguments into locals of new arec
        for i in range(0, self._argument_count):
            new_arec.set_local_at(i, activation_record.pop())

        interpreter.interpret(self, new_arec)

    def get_class(self, universe):
        return universe.methodClass

    def disassemble(self):
        return Disassembler().disassemble(self)
