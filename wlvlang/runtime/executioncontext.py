from wlvlang.interpreter.interpreter import Interpreter
from wlvlang.interpreter.activationrecord import ActivationRecord
from wlvlang.interpreter.bytecode import bytecode_names
from rpythonex.rdequeue import CircularWorkStealingDeque

from wlvlang.interpreter.space import ObjectSpace

from rpython.rlib import jit
from wlvlang.runtime.os_thread import start_new_thread

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


class Universe(object):
    def __init__(self, thread_count, space):
        self._thread_pool = [-1] * (thread_count - 1)
        self._thread_count = thread_count - 1
        self.main_scheduler = ThreadLocalSched(space, self)
        self.space = space


    def start(self, main_method, arg_local, arg_array):
        self._bootstrap(main_method, arg_local, arg_array)

        for i in range(0, self._thread_count - 1):
            self._thread_pool[i] = start_new_thread(self.space, self, (self))

        self._main_sched()


    def _bootstrap(self, main_method, arg_local, arg_array):
        frame = ActivationRecord(method=main_method)
        frame.set_local_at(arg_local, arg_array)

        main_task = Task(self.main_scheduler)
        main_task.set_top_frame(frame)

        self.main_scheduler.add_ready_task(main_task)


    def _main_sched(self):
        self.main_scheduler.run()


    @staticmethod
    def run(args, space):
        scheduler = ThreadLocalSched(space, args[0])
        scheduler.run()

class ThreadLocalSched(object):
    """ Describes a scheduler for a number of tasks multiplexed onto a single OS Thread """

    def __init__(self, space, universe):
        self.ready_tasks = CircularWorkStealingDeque(4)
        self.yielding_tasks = CircularWorkStealingDeque(4)

        # Points to the current running context in this execution context
        self._context_pointer = -1

        # Interpreters are mostly stateless (they simply contain code and a
        # reference to a space), they can be shared between local tasks in an
        # execution context
        self.interpreter = Interpreter(space)

    def add_ready_task(self, task):
        self.ready_tasks.push_bottom(task)

    def _get_next_task(self):
        task = self.ready_tasks.pop_bottom()

        if task is None:
            yielding_task = self.yielding_tasks.pop_bottom()
            if yielding_task is None:
                return None

            return yielding_task
        return task

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
            task = self._get_next_task()
            if task is None:
                return

            self.run_task(task)

            if not task.get_state() == Interpreter.HALT:
                self.yielding_tasks.push_bottom(task)


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
