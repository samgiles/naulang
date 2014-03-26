from wlvlang.interpreter.interpreter import Interpreter
from wlvlang.interpreter.frame import Frame
from wlvlang.interpreter.bytecode import bytecode_names
from rpythonex.rdequeue import CircularWorkStealingDeque
from rpythonex.rthread import thread_join

from rpython.rlib import jit, rthread, rrandom
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

class Universe(object):
    def __init__(self, thread_count, space):
        self._rand = rrandom.Random(9)
        self._thread_count = thread_count + 1
        self._thread_local_scheds = [None] * (self._thread_count + 1)
        self._thread_pool = [-1] * (self._thread_count)
        self.space = space


    def register_scheduler(self, identifier, scheduler):
        index = int(identifier) % self._thread_count
        self._thread_local_scheds[index] = scheduler

    def steal(self):
        index = int(self._rand.random() * self._thread_count) % self._thread_count
        sched = self._thread_local_scheds[index]

        if sched is not None:
            return sched.steal()

        return None

    def start(self, main_method, arg_local, arg_array):
        self.main_scheduler = ThreadLocalSched(self.space, self)
        self._bootstrap(main_method, arg_local, arg_array)
        self._thread_pool = [-1] * (self._thread_count)

        for i in range(1, self._thread_count):
            self._thread_pool[i] = int(start_new_thread(self.space, self, [self]))

        identifier = rthread.get_ident()
        self.register_scheduler(identifier, self.main_scheduler)
        self._main_sched()

        for i in range(1, self._thread_count):
            thread_join(self._thread_pool[i])


    def _bootstrap(self, main_method, arg_local, arg_array):
        frame = Frame(method=main_method)
        frame.set_local_at(arg_local, arg_array)

        main_task = Task(self.main_scheduler)
        main_task.set_top_frame(frame)

        self.main_scheduler.add_ready_task(main_task)


    def _main_sched(self):
        self.main_scheduler.run()


    @staticmethod
    def run(args, space):
        assert len(args) == 1
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

        self.universe = universe


    def add_ready_task(self, task):
        self.ready_tasks.push_bottom(task)

    def _get_next_task(self):
        task = self.ready_tasks.pop_bottom()

        if task is None:
            yielding_task = self.yielding_tasks.pop_bottom()
            if yielding_task is None:
                return self.universe.steal()

            return yielding_task

        return task

    def steal(self):
        task = self.ready_tasks.steal()
        if task is None:
            task = self.yielding_tasks.steal()

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
        self.universe.register_scheduler(rthread.get_ident(), self)
        while True:
            task = self._get_next_task()
            if task is None:
                return

            self.run_task(task)

            if task.get_state() == Interpreter.YIELD:
                self.yielding_tasks.push_bottom(task)
            elif task.get_state() != Interpreter.HALT:
                self.ready_tasks.push_bottom(task)


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
            frame.set_previous_frame(top_frame)

        self.top_frame = frame

    def restore_previous_frame(self):
        self.top_frame = self.get_top_frame().get_previous_frame()

    def get_current_method(self):
        return self.top_frame.method

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def __eq__(self, other):
        return self._state == other._state and self.top_frame == other.top_frame and self.parent == other.parent
