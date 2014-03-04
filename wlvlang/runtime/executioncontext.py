from rpython.rlib import jit

from wlvlang.interpreter.interpreter import Interpreter


_max_interleaved_interp = 10

class ExecutionContext(object):
    """ Describes an execution context for a task """

    FRESH     = 0
    SUSPENDED = 1
    RUNNING   = 2
    DEAD      = 3

    def __init__(self, space):
        self.state = ExecutionContext.FRESH
        self.contexts = [None] * _max_interleaved_interp
        self._context_pointer = 0
        self._insert_next = 0

        self.interpreter = Interpreter(space)

        # Index of the previous running interpreter
        self._last_interpreter = 0

    def add_context(self, context):
        self.contexts[self._insert_next] = context

        i = 0
        while i < _max_interleaved_interp:

            if self.contexts[i] is None:
                self._insert_next = i
                return

            if self.contexts[i].get_state() == Interpreter.HALT:
                self._insert_next = i
                return

            i += 1

        # TODO: If flow reaches here, next insert will fail or overwrite a
        # running context

    def _get_next_interpreter(self):
        pass

    def run_context(self, index):
        context = self.contexts[index]
        while self.interpreter.interpreter_step(context):
            pass

class InterpreterContext(object):
    def __init__(self):
        self._pc = 0
        self._state = Interpreter.CONTINUE
        self.top_frame = jit.vref_None

    def get_top_frame(self):
        return self.top_frame

    def set_top_frame(self, frame):
        # Save the state: pc
        # Then set the top frame, this context
        # will then continue from the method call
        top_frame = self.get_top_frame()

        if top_frame is not jit.vref_None:
            top_frame.saved_pc = self._pc
            frame.set_previous_record(top_frame)

        self.top_frame = frame
        self._pc = 0

    def restore_previous_frame(self):
        self.top_frame = self.get_top_frame().get_previous_record()
        self._pc = self.top_frame.saved_pc

    def get_current_method(self):
        return self.top_frame.method

    def set_pc(self, pc):
        self._pc = pc

    def get_pc(self):
        return self._pc

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state
