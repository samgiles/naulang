from rpythonex.rdequeue import CircularWorkStealingDeque as Deq

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
    import pdb;pdb.set_trace()

    for i in range((0x1 << deq_logsize) + 1):
        deq.push_bottom(i)

    for i in range((0x1 << deq_logsize), -1, -1):
        assert deq.pop_bottom() == i
