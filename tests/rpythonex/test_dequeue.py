from rpythonex.rdequeue import CircularWorkStealingDeque as Deq

def test_init_to_size():
    deq = Deq(4)
    assert deq.size() == 16
