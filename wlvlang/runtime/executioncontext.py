from wlvlang.interpreter.interpreter import Interpreter
from wlvlang.interpreter.bytecode import bytecode_names
from rpythonex.rdequeue import Dequeue

from rpython.rlib import jit

# For the sake of experimentation this is hardcoded
# deadlocks abound when the number of tasks exceeds this
_max_interleaved_interp = 10

def get_printable_location(pc, sched, method):
    return "%d: %s" % (pc, bytecode_names[method.get_bytecode(pc)])

jitdriver = jit.JitDriver(
        greens=['pc', 'sched', 'method'],
        reds=['frame', 'task'],
        virtualizables=['frame'],
        get_printable_location=get_printable_location
    )

class DeadLockedException(Exception):
    pass

class ThreadLocalSched(object):
    """ Describes a scheduler for a number of tasks multiplexed onto a single OS Thread """

    def __init__(self, space):
        self.ready_tasks = Dequeue()

        # Points to the current running context in this execution context
        self._context_pointer = -1

        # Interpreters are mostly stateless (they simply contain code and a
        # reference to a space), they can be shared between local tasks in an
        # execution context
        self.interpreter = Interpreter(space)

        # Used to detect for deadlocks every so often rather than every task
        # switch
        self._deadlock_counter = 0

        self._task_count = 0

    def add_ready_task(self, task):
        node = self.ready_tasks.create_node(task)
        self.ready_tasks.push_bottom(node)

    def _get_next_ready_task(self):
        node = self.ready_tasks.pop_bottom()
        if node is None:
            return None
        return node.value

    def run_task(self, task):
        assert task is not None
        oldpc = 0

        while True:
            pc = task.get_top_frame().get_pc()
            method = task.get_current_method()

            if pc < oldpc:
                jitdriver.can_enter_jit(
                    pc=pc,
                    sched=self,
                    method=method,
                    task=task,
                    frame=task.get_top_frame(),
                )

            oldpc = pc

            jitdriver.jit_merge_point(
                    pc=pc,
                    sched=self,
                    method=method,
                    task=task,
                    frame=task.get_top_frame(),
                )

            should_continue = self.interpreter.interpreter_step(task)

            if not should_continue:
                return


    def run(self):
        while True:
            task = self._get_next_ready_task()
            if task is None:
                return

            self.run_task(task)
            node = self.ready_tasks.create_node(task)
            self.ready_tasks.push_top(node)


class Task(object):
    _immutable_fields_ = ["parent"]

    def __init__(self, owning_scheduler, parent=None):
        """ Create a new task

            kwargs:
                parent  -- The task that spawned this task.
        """
        self._state = Interpreter.CONTINUE
        self.top_frame = None
        self.parent = parent
        self.sched = owning_scheduler

    def get_top_frame(self):
        return self.top_frame

    def set_top_frame(self, frame):
        # Save the state: pc
        # Then set the top frame, this context
        # will then continue from the method call
        top_frame = self.get_top_frame()

        if top_frame is not None:
            frame.set_previous_record(top_frame)

        self.top_frame = frame

    def restore_previous_frame(self):
        self.top_frame = self.get_top_frame().get_previous_record()

    def get_current_method(self):
        return self.top_frame.method

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def __eq__(self, other):
        return self._state == other._state and self.top_frame == other.top_frame and self.parent == other.parent
