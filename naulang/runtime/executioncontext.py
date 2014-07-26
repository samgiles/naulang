from naulang.interpreter.interpreter import Interpreter
from naulang.interpreter.error import NauRuntimeError
from naulang.interpreter.frame import Frame
from rpythonex.rdequeue import CircularWorkStealingDeque, SimpleDequeue
from rpythonex.rcircular import CircularArray

from rpython.rlib import jit, rrandom


def get_printable_location(pc, sched, method):
    return "TODO:"

jitdriver = jit.JitDriver(
    greens=['pc', 'sched', 'method'],
    reds=['frame', 'task'],
    virtualizables=['frame'],
    get_printable_location=get_printable_location
)


def get_printable_location_taskdriver(sched):
    return "Scheduler Loop"

taskjitdriver = jit.JitDriver(
    greens=['sched'],
    reds='auto',
    get_printable_location=get_printable_location_taskdriver)


class Universe(object):

    def __init__(self, thread_count, space):
        self._rand = rrandom.Random(9)
        self._thread_count = thread_count + 1
        self._thread_local_scheds = [None] * (self._thread_count + 1)
        self.space = space

    def register_scheduler(self, identifier, scheduler):
        index = int(identifier) % self._thread_count
        self._thread_local_scheds[index] = scheduler

    def start(self, main_method, arg_local, arg_array):
        self.main_scheduler = ThreadLocalSched(self.space, self)
        self._bootstrap(main_method, arg_local, arg_array)

        self.register_scheduler(0, self.main_scheduler)
        self._main_sched()

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


class TaskCircularArray(CircularArray):

    def _create_new_instance(self, new_size):
        return TaskCircularArray(new_size)


class TaskDequeue(CircularWorkStealingDeque):

    def _initialise_array(self, log_initial_size):
        return TaskCircularArray(log_initial_size)


class ThreadLocalSched(object):

    """ Describes a scheduler for a number of tasks multiplexed onto a single OS Thread """
    _immutable_fields_ = ["interpreter", "universe", "ready_tasks", "yielding_tasks"]

    def __init__(self, space, universe):
        self.ready_tasks = SimpleDequeue()
        self.yielding_tasks = SimpleDequeue()

        # Interpreters are mostly stateless (they simply contain code and a
        # reference to a space), they can be shared between local tasks in an
        # execution context
        self.interpreter = Interpreter(space)

        self.universe = universe

    def add_ready_task(self, task):
        self.ready_tasks.push_bottom(task)

    def _reload_yielding_tasks(self):
        yielding_taskb = None
        while True:
            yielding_taska = self.yielding_tasks.steal()
            if yielding_taska is None:
                break

            yielding_taskb = self.yielding_tasks.steal()
            if yielding_taskb is None:
                return yielding_taska

            self.ready_tasks.push_bottom(yielding_taska)
            self.ready_tasks.push_bottom(yielding_taskb)

        return yielding_taskb

    def _get_next_task(self):
        task = self.ready_tasks.pop_bottom()

        if task is not None:
            return task

        return self._reload_yielding_tasks()

    def _can_enter_jit(self, pc, method, task, frame):
        jitdriver.can_enter_jit(
            pc=pc,
            sched=self,
            method=method,
            task=task,
            frame=frame,
        )

    @jit.unroll_safe
    def run_task(self, task):
        assert task is not None

        last_pc = 0
        last_function = None

        try:

            while True:
                frame = task.get_top_frame()
                pc = frame.get_pc()
                method = task.get_current_method()

                still_in_function = method is last_function
                if pc < last_pc and still_in_function:
                    self._can_enter_jit(pc, method, task, frame)

                jitdriver.jit_merge_point(
                    pc=pc,
                    sched=self,
                    method=method,
                    task=task,
                    frame=frame,
                )

                last_pc = pc
                last_function = method

                should_continue = self.interpreter.interpreter_step(pc, method, frame, task)

                if not should_continue:
                    return
        except NauRuntimeError as e:
            # add the appropriate information to the error
            e.pc = last_pc
            e.frame = task.get_top_frame()
            e.method = method = task.get_current_method()
            raise e

    def run(self):
        while True:

            task = self._get_next_task()
            if task is None:
                return

            self.run_task(task)

            if task.get_state() == Interpreter.YIELD:
                self.yielding_tasks.push_bottom(task)
            elif task.get_state() == Interpreter.SUSPEND:
                continue
            elif task.get_state() is not Interpreter.HALT:
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

    def reschedule(self):
        self.sched.add_ready_task(self)

    def __eq__(self, other):
        return self._state == other._state and self.top_frame == other.top_frame and self.parent == other.parent
