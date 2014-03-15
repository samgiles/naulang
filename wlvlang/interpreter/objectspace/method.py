from wlvlang.interpreter.objectspace.object import Object
from wlvlang.interpreter.activationrecord import ActivationRecord

from rpython.rlib import jit
from rpython.rlib import rthread

class Method(Object):
    """ Defines a Method in wlvlang. """

    _immutable_fields_ = [
            "locals[*]",
            "literals[*]",
            "bytecodes[*]",
            "stack_depth",
        ]

    def __init__(self, literals, locals, bytecodes, stack_depth, argument_count=0):
        self.literals = literals
        self.locals = locals
        self.bytecodes = bytecodes
        self.argument_count = argument_count
        self.enclosing_arec = None
        self.stack_depth = stack_depth

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
        return Method(self.literals, self.locals, self.bytecodes, self.stack_depth, argument_count=self.argument_count)

    def async_invoke(self, context, interpreter):
        self.invoke(context, interpreter)

    def invoke(self, current_task):
        jit.promote(self)

        frame = ActivationRecord(previous_record=current_task.get_top_frame(), method=self, access_link=self.get_enclosing_arec())

        # Push arguments into locals of new arec
        for i in range(0, self.argument_count):
            frame.set_local_at(i, current_task.get_top_frame().pop())

        current_task.set_top_frame(frame)

    def get_class(self, space):
        return space.methodClass

    def __repr__(self):
        return "Method<%r>: closed by: <%r>" % (hex(id(self)), hex(id(self.enclosing_arec)))
