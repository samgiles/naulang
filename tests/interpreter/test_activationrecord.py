import pytest
from wlvlang.interpreter.activationrecord import ActivationRecord


def test_is_root_record():
    subject = ActivationRecord([], 0, 0, 0, None)

    assert(True == subject.is_root_record())

def test_get_literals():

    # Usually locals will always be of type vmobjects.Object
    # But since this is running under normal python for testing and
    # not RPython, it's fine to use normal primitives for this test case
    # The first 4 slots are spaces for hypothetical 'locals'
    # The final 3 are hypothetical literals
    locals = [None, None, None, None, 10, 100, 1000]
    locals_size = 4
    literals_size = 3

    arec = ActivationRecord(locals, locals_size, literals_size, 0, None)

    assert arec.get_literal_at(0) == 10
    assert arec.get_literal_at(1) == 100
    assert arec.get_literal_at(2) == 1000

def test_get_locals():
    locals = [10, 100, 1000, 10000, None, None, None]
    locals_size = 4
    literals_size = 3

    arec = ActivationRecord(locals, locals_size, literals_size, 0, None)

    assert arec.get_local_at(0) == 10
    assert arec.get_local_at(1) == 100
    assert arec.get_local_at(2) == 1000
    assert arec.get_local_at(3) == 10000

def test_push_advances_stackpointer():
    arec = ActivationRecord([], 0, 0, 10, None)

    current_stack_pointer = arec._stack_pointer
    arec.push(10)
    assert arec._stack_pointer == current_stack_pointer + 1

