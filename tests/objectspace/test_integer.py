import pytest

from wlvlang.interpreter.activationrecord import ActivationRecord
from wlvlang.vmobjects.integer import Integer
from wlvlang.vmobjects.boolean import Boolean
from wlvlang.vmobjects.primitives.integer_primitive import _mul, _add, _div, _mod, _sub, _eq

def test_get_value():
    subject = Integer(10)

    assert(subject.get_value() == 10)

def setup_primitive_test(left_int, right_int):
    arec = ActivationRecord(2, None)

    arec.push(Integer(left_int))
    arec.push(Integer(right_int))

    return arec


def test_mul_primitive():
    arec = setup_primitive_test(100, 200)

    _mul(None, arec, None)

    value = arec.pop()
    assert(value.get_value() == 20000)

def test_add_primitive():
    arec = setup_primitive_test(100, 200)

    _add(None, arec, None)

    value = arec.pop()
    assert(value.get_value() == 300)

def test_sub_primitive():
    arec = setup_primitive_test(100, 200)

    _sub(None, arec, None)

    value = arec.pop()
    assert(value.get_value() == -100)

def test_div_primitive():
    arec = setup_primitive_test(100, 50)

    _div(None, arec, None)

    value = arec.pop()
    assert(value.get_value() == 2)

def test_mod_primitive():
    arec = setup_primitive_test(100, 3)

    _mod(None, arec, None)

    value = arec.pop()
    assert(value.get_value() == 1)

def test_eq_primitive_true():
    arec = setup_primitive_test(10, 10)

    _eq(None, arec, None)

    value = arec.pop()
    assert(isinstance(value, Boolean))
    assert(value.get_value() == True)

def test_eq_primitive_false():
    arec = setup_primitive_test(11, 10)

    _eq(None, arec, None)

    value = arec.pop()
    assert(isinstance(value, Boolean))
    assert(value.get_value() == False)
