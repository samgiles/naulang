import pytest

from wlvlang.interpreter.activationrecord import ActivationRecord
from wlvlang.interpreter.objectspace.method import Method

def test_is_root_record():
    method = Method([], 0, [], 10)
    arec = ActivationRecord(previous_record=None, method=method, access_link=None)

    assert(True == arec.is_root_record())

def test_get_literals():

    # Usually locals will always be of type vmobjects.Object
    # But since this is running under normal python for testing and
    # not RPython, it's fine to use normal primitives for this test case
    literals= [10, 100, 1000]
    method = Method(literals, 4, [], 10)
    arec = ActivationRecord(previous_record=None, method=method, access_link=None)


    assert arec.get_literal_at(0) == 10
    assert arec.get_literal_at(1) == 100
    assert arec.get_literal_at(2) == 1000

def test_get_locals():
    method = Method([], 4, [], 10)
    arec = ActivationRecord(previous_record=None, method=method, access_link=None)

    arec.set_local_at(0, 10)
    arec.set_local_at(1, 100)
    arec.set_local_at(2, 1000)
    arec.set_local_at(3, 10000)

    assert arec.get_local_at(0) == 10
    assert arec.get_local_at(1) == 100
    assert arec.get_local_at(2) == 1000
    assert arec.get_local_at(3) == 10000

def test_set_local_at():
    locals = [10, 100, 1000, 10000]

    method = Method([], 4, [], 10)
    arec = ActivationRecord(previous_record=None, method=method, access_link=None)
    arec.set_local_at(1, 200)
    assert arec.get_local_at(1) == 200

def test_push_advances_stackpointer():
    method = Method([], 0, [], 10)
    arec = ActivationRecord(previous_record=None, method=method, access_link=None)

    current_stack_pointer = arec._stack_pointer
    arec.push(10)
    assert arec._stack_pointer == current_stack_pointer + 1

def test_pop_decreases_stackpointer():
    method = Method([], 0, [], 10)
    arec = ActivationRecord(previous_record=None, method=method, access_link=None)
    # Push a value on the stack in order to pop it off
    arec.push(10)
    current_stack_pointer = arec._stack_pointer
    arec.pop()
    assert arec._stack_pointer == current_stack_pointer - 1

def test_push_pop_from_stack():
    method = Method([], 0, [], 10)
    arec = ActivationRecord(previous_record=None, method=method, access_link=None)
    # Push a value on the stack in order to pop it off
    arec.push(10)
    assert 10 == arec.pop()

def test_peek_at_stack():
    method = Method([], 0, [], 10)
    arec = ActivationRecord(previous_record=None, method=method, access_link=None)
    # Push a value on the stack in order to pop it off
    arec.push(10)
    assert 10 == arec.peek()
    assert 10 == arec.peek()
