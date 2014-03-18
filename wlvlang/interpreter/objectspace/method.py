from wlvlang.interpreter.objectspace.object import Object
from wlvlang.interpreter.activationrecord import ActivationRecord
from rpython.rlib import jit

class Method(Object):
    """ Defines a Method in wlvlang. """

    _immutable_fields_ = [
            "locals[*]",
            "literals[*]",
            "bytecodes[*]",
            "stack_depth",
        ]

    def __init__(self, literals, local_count, bytecodes, stack_depth, argument_count=0):
        self.literals = literals
        self.local_count = local_count
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
        return Method(self.literals, self.local_count, self.bytecodes, self.stack_depth, argument_count=self.argument_count)

    def _create_new_frame(self, task, is_async=False):
        if is_async:
            previous_frame = None
        else:
            previous_frame = task.get_top_frame()

        new_frame = ActivationRecord(previous_record=previous_frame, method=self, access_link=self.get_enclosing_arec())

        # Push arguments into locals of new arec
        for i in range(0, self.argument_count):
            new_frame.set_local_at(i, task.get_top_frame().pop())

        return new_frame

    def async_invoke(self, task):
        from wlvlang.runtime.executioncontext import Task
        frame = self._create_new_frame(task, is_async=True)
        new_task = Task(task.sched, parent=task)
        new_task.set_top_frame(frame)
        task.sched.add_task(new_task)

    def invoke(self, current_task):
        jit.promote(self)
        new_frame = self._create_new_frame(current_task, is_async=False)
        current_task.set_top_frame(new_frame)

    def get_class(self, space):
        return space.methodClass

    def __repr__(self):
        return "Method<%r>: closed by: <%r>" % (hex(id(self)), hex(id(self.enclosing_arec)))
