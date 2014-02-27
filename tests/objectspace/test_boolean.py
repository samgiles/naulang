import pytest

from wlvlang.vmobjects.boolean import Boolean
from wlvlang.interpreter.activationrecord import ActivationRecord
from wlvlang.vmobjects.primitives.boolean_primitive import _eq, _or, _and

def test_get_value():
    subjecta = Boolean(True)
    subjectb = Boolean(False)

    assert(subjecta.get_value() == True)
    assert(subjectb.get_value() == False)

def setup_primitive_test(left_val, right_val):
    arec = ActivationRecord(2, None)

    arec.push(Boolean(left_val))
    arec.push(Boolean(right_val))

    return arec

def test_eq_primitive_true_true():
    arec = setup_primitive_test(True, True)

    _eq(None, arec, None)

    value = arec.pop()
    assert(value.get_value() == True)

def test_eq_primitive_true_false():
    arec = setup_primitive_test(True, False)

    _eq(None, arec, None)

    value = arec.pop()
    assert(value.get_value() == False)

def test_eq_primitive_false_true():
    arec = setup_primitive_test(False, True)

    _eq(None, arec, None)

    value = arec.pop()
    assert(value.get_value() == False)

def test_or_primitive_true_true():
    arec = setup_primitive_test(True, True)

    _or(None, arec, None)

    value = arec.pop()
    assert(value.get_value() == True)

def test_or_primitive_true_false():
    arec = setup_primitive_test(True, False)

    _or(None, arec, None)

    value = arec.pop()
    assert(value.get_value() == True)

def test_or_primitive_false_true():
    arec = setup_primitive_test(False, True)

    _or(None, arec, None)

    value = arec.pop()
    assert(value.get_value() == True)

def test_or_primitive_false_false():
    arec = setup_primitive_test(False, False)

    _or(None, arec, None)

    value = arec.pop()
    assert(value.get_value() == False)

def test_and_primitive_true_true():
    arec = setup_primitive_test(True, True)

    _and(None, arec, None)

    value = arec.pop()
    assert(value.get_value() == True)

def test_and_primitive_false_true():
    arec = setup_primitive_test(False, True)

    _and(None, arec, None)
    value = arec.pop()
    assert(value.get_value() == False)
