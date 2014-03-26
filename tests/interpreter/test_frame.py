from wlvlang.interpreter.frame import Frame
from wlvlang.interpreter.objectspace.method import Method

def test_is_root_frame():
    method = Method([], 0, [], 10)
    frame = Frame(previous_frame=None, method=method, access_link=None)

    assert(True == frame.is_root_frame())

def test_get_literals():

    # Usually locals will always be of type vmobjects.Object
    # But since this is running under normal python for testing and
    # not RPython, it's fine to use normal primitives for this test case
    literals= [10, 100, 1000]
    method = Method(literals, 4, [], 10)
    frame = Frame(previous_frame=None, method=method, access_link=None)


    assert frame.get_literal_at(0) == 10
    assert frame.get_literal_at(1) == 100
    assert frame.get_literal_at(2) == 1000

def test_get_locals():
    method = Method([], 4, [], 10)
    frame = Frame(previous_frame=None, method=method, access_link=None)

    frame.set_local_at(0, 10)
    frame.set_local_at(1, 100)
    frame.set_local_at(2, 1000)
    frame.set_local_at(3, 10000)

    assert frame.get_local_at(0) == 10
    assert frame.get_local_at(1) == 100
    assert frame.get_local_at(2) == 1000
    assert frame.get_local_at(3) == 10000

def test_set_local_at():
    method = Method([], 4, [], 10)
    frame = Frame(previous_frame=None, method=method, access_link=None)
    frame.set_local_at(1, 200)
    assert frame.get_local_at(1) == 200

def test_push_advances_stackpointer():
    method = Method([], 0, [], 10)
    frame = Frame(previous_frame=None, method=method, access_link=None)

    current_stack_pointer = frame._stack_pointer
    frame.push(10)
    assert frame._stack_pointer == current_stack_pointer + 1

def test_pop_decreases_stackpointer():
    method = Method([], 0, [], 10)
    frame = Frame(previous_frame=None, method=method, access_link=None)
    # Push a value on the stack in order to pop it off
    frame.push(10)
    current_stack_pointer = frame._stack_pointer
    frame.pop()
    assert frame._stack_pointer == current_stack_pointer - 1

def test_push_pop_from_stack():
    method = Method([], 0, [], 10)
    frame = Frame(previous_frame=None, method=method, access_link=None)
    # Push a value on the stack in order to pop it off
    frame.push(10)
    assert 10 == frame.pop()

def test_peek_at_stack():
    method = Method([], 0, [], 10)
    frame = Frame(previous_frame=None, method=method, access_link=None)
    # Push a value on the stack in order to pop it off
    frame.push(10)
    assert 10 == frame.peek()
    assert 10 == frame.peek()
