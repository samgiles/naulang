from wlvlang.vmobjects.object import Object
from wlvlang.compiler.disassembler import Disassembler

from wlvlang.interpreter.activationrecord import ActivationRecord
from rpython.rlib import jit

import copy

class Method(Object):
    """ Defines a Method in the wlvlang-vm. """

    _immutable_fields_ = ['_bytecodes', '_signature']


    def __init__(self, signature, literals, locals, bytecodes, argument_count=0):
        self._literals = literals
        self._locals = locals
        self._bytecodes = bytecodes
        self._signature = signature
        self._argument_count = argument_count
        self._enclosing_arec = None

    def set_enclosing_arec(self, arec):
        self._enclosing_arec = arec

    def get_enclosing_arec(self):
        return self._enclosing_arec

    def get_bytecode(self, index):
        assert 0 <= index and index < len(self._bytecodes)
        return self._bytecodes[index]

    def get_literals(self):
        return self._literals

    def get_signature(self):
        return self._signature

    def copy(self):
        return Method(self._signature, self._literals, self._locals, self._bytecodes, argument_count=self._argument_count)

    def invoke(self, activation_record, interpreter):
        new_arec = ActivationRecord(self._locals + self._literals, len(self._locals), len(self._literals), 200, activation_record, access_link=self.get_enclosing_arec())

        # Push arguments into locals of new arec
        for i in range(0, self._argument_count):
            new_arec.set_local_at(i, activation_record.pop())

        interpreter.interpret(self, new_arec)

    def get_class(self, universe):
        return universe.methodClass

    def disassemble(self):
        return Disassembler().disassemble(self)

    def __repr__(self):
        return "vmobjects.Method<%r>: closed by: <%r>" % (id(self), id(self._enclosing_arec))
