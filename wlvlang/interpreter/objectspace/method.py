from wlvlang.interpreter.objectspace.object import Object
from wlvlang.interpreter.activationrecord import ActivationRecord

class Method(Object):
    """ Defines a Method in wlvlang. """

    def __init__(self, literals, locals, bytecodes, argument_count=0):
        self.literals = literals
        self.locals = locals
        self.bytecodes = bytecodes
        self.argument_count = argument_count
        self.enclosing_arec = None

    def set_enclosing_arec(self, arec):
        self.enclosing_arec = arec

    def get_enclosing_arec(self):
        return self.enclosing_arec

    def get_bytecode(self, index):
        assert 0 <= index and index < len(self.bytecodes)
        return self.bytecodes[index]

    def get_literals(self):
        return self.literals

    def copy(self):
        return Method(self.literals, self.locals, self.bytecodes, argument_count=self.argument_count)

    def invoke(self, activation_record, interpreter):

        # TODO Calculate stack depth
        new_arec = ActivationRecord(self.locals + self.literals, len(self.locals), len(self.literals), 200, activation_record, access_link=self.get_enclosing_arec())

        # Push arguments into locals of new arec
        for i in range(0, self.argument_count):
            new_arec.set_local_at(i, activation_record.pop())

        interpreter.interpret(self, new_arec)

    def get_class(self, space):
        return space.methodClass

    def __repr__(self):
        return "Method<%r>: closed by: <%r>" % (hex(id(self)), hex(id(self.enclosing_arec)))
