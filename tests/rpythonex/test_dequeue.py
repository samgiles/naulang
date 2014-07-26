from rpythonex.rdequeue import CircularWorkStealingDeque
from rpythonex.rcircular import CircularArray


class TestCircularArray(CircularArray):

    def _create_new_instance(self, new_size):
        return TestCircularArray(new_size)


class Deq(CircularWorkStealingDeque):

    def _initialise_array(self, log_initial_size):
        return TestCircularArray(log_initial_size)


def test_init_to_size():
    deq = Deq(4)
    assert deq.size() == 16


def test_push_bottom():
    deq = Deq(4)
    deq.push_bottom(190)

    assert deq.pop_bottom() == 190


def test_push_bottom_filled():
    deq_logsize = 4
    deq = Deq(deq_logsize)

    for i in range((0x1 << deq_logsize) + 1):
        deq.push_bottom(i)

    for i in range((0x1 << deq_logsize), -1, -1):
        assert deq.pop_bottom() == i


def test_steal():
    deq_logsize = 4
    deq = Deq(deq_logsize)

    for i in range((0x1 << deq_logsize) - 1):
        deq.push_bottom(i)

    for i in range((0x1 << deq_logsize) - 1):
        assert deq.steal() == i


def test_steal_and_push_doesnt_grow():
    deq_logsize = 4
    deq = Deq(deq_logsize)

    for i in range((0x1 << deq_logsize) - 1):
        deq.push_bottom(i)

    # Assert that the queue has not grown in size (even though it is full)
    assert deq.size() == 0x1 << deq_logsize
    assert deq.steal() == 0

    deq.push_bottom((0x1 << deq_logsize) - 1)
    assert deq.size() == 0x1 << deq_logsize

    for i in range((0x1 << deq_logsize) - 1, 0, -1):
        assert deq.pop_bottom() == i
