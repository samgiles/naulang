from naulang.runtime.executioncontext import ThreadLocalSched, Task, Universe
from naulang.interpreter.space import ObjectSpace


def test_add_task():
    """ Expected:
            Adding two tasks to an empty Scheduler should result in the first
            task being set to the current task in the Scheduler,
            then a second task added should fill the next slot in the scheduler
            and upon calling the internal _get_next_task we should get this task from the
            scheduler.

        Note:
            If you've implemented a new Scheduler you've probably broken this test, that's fine,
            just refactor to keep the old functionality as a strategy or something
    """
    space = ObjectSpace()
    sched = ThreadLocalSched(space, Universe(0, space))
    task = Task(sched)
    sched.add_ready_task(Task(sched))
    sched.add_ready_task(task)
    assert task is sched._get_next_task()
