from wlvlang.interpreter.objectspace.object import Object
from wlvlang.interpreter.frame import Frame
from rpython.rlib import jit

class Method(Object):
    """ Defines a Method in wlvlang. """

    _immutable_fields_ = [
            "locals",
            "literals",
            "bytecodes",
            "stack_depth",
        ]

    def __init__(self, literals, local_count, bytecodes, stack_depth, argument_count=0):
        self.literals = literals
        self.local_count = local_count
        self.bytecodes = bytecodes
        self.argument_count = argument_count
        self.enclosing_frame = None
        self.stack_depth = stack_depth

    def set_enclosing_frame(self, frame):
        self.enclosing_frame = frame

    def get_enclosing_frame(self):
        return self.enclosing_frame

    def get_bytecode(self, index):
        index = jit.promote(index)
        assert 0 <= index and index < len(self.bytecodes)
        return jit.promote(self.bytecodes[index])

    def get_literals(self):
        return self.literals

    def copy(self):
        return Method(self.literals, self.local_count, self.bytecodes, self.stack_depth, argument_count=self.argument_count)

    @jit.unroll_safe
    def _create_new_frame(self, previous_frame, is_async=False):
        new_frame = Frame(previous_frame=previous_frame if not is_async else None, method=self, access_link=self.get_enclosing_frame())

        # Push arguments into locals of new frame in reverse order
        arg_number = self.argument_count - 1
        while arg_number >= 0:
            new_frame.set_local_at(arg_number, previous_frame.pop())
            arg_number -= 1

        return new_frame

    def async_invoke(self, task):
        from wlvlang.runtime.executioncontext import Task
        frame = self._create_new_frame(previous_frame=task.get_top_frame(), is_async=True)
        new_task = Task(task.sched, parent=task)
        new_task.set_top_frame(frame)
        task.sched.add_ready_task(new_task)

    def invoke(self, current_frame, current_task):
        new_frame = self._create_new_frame(previous_frame=current_frame)
        current_task.set_top_frame(new_frame)

    def get_class(self, space):
        return space.methodClass

    def __repr__(self):
        return "Method<%r>: closed by: <%r>" % (hex(id(self)), hex(id(self.enclosing_frame)))
