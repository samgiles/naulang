from wlvlang.interpreter.interpreter import Interpreter


_max_interleaved_interp = 10

class ThreadLocalSched(object):
    """ Describes a scheduler for a number of tasks multiplexed onto a single OS Thread """

    def __init__(self, space):
        self.tasks = [None] * _max_interleaved_interp

        # Points to the current running context in this execution context
        self._context_pointer = 0

        # Points to the slot in which to insert the next context into the
        # execution context
        self._insert_next = 0

        # Interpreters are mostly stateless (they simply contain code and a
        # reference to a space), they can be shared between local tasks in an
        # execution context
        self.interpreter = Interpreter(space)

    def add_task(self, task):
        self.tasks[self._insert_next] = task
        self._update_insert_next();

    def _update_insert_next(self):
        slot = 0
        while slot < _max_interleaved_interp:

            task_slot_usable = self.tasks[slot] is None or self.tasks[slot].get_state() == Interpreter.HALT

            if task_slot_usable:
                self._insert_next = slot
                return

            slot += 1

    def _get_next_task(self):

        # Assume th next slot is the current +1
        slot = self._context_pointer + 1;

        # But check we haven't gone beyond the bounds of the task list
        if not slot < _max_interleaved_interp:
            slot = 0

        while slot < _max_interleaved_interp:

            task_slot_runnable = self.tasks[slot] is not None and self.tasks[slot].get_state() != Interpreter.HALT

            if task_slot_runnable:
                return self.tasks[slot]

            slot += 1

    def run_task(self, slot):
        task = self.tasks[slot]
        while self.interpreter.interpreter_step(task):
            pass

class Task(object):
    def __init__(self):
        self._pc = 0
        self._state = Interpreter.CONTINUE
        self.top_frame = None

    def get_top_frame(self):
        return self.top_frame

    def set_top_frame(self, frame):
        # Save the state: pc
        # Then set the top frame, this context
        # will then continue from the method call
        top_frame = self.get_top_frame()

        if top_frame is not None:
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
