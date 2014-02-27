import pytest

from wlvlang.interpreter.activationrecord import ActivationRecord
from wlvlang.interpreter.objectspace.integer import Integer
from wlvlang.interpreter.objectspace.boolean import Boolean
from wlvlang.interpreter.objectspace.primitives.integer_primitive import _mul, _add, _div, _mod, _sub, _eq

from wlvlang.interpreter.interpreter import Interpreter
from wlvlang.interpreter.space import ObjectSpace

def test_get_value():
    subject = Integer(42)

    assert subject.get_integer_value() == 42

def setup_primitive_test(left_int, right_int):
    arec = ActivationRecord([], [], 2, None)

    arec.push(Integer(left_int))
    arec.push(Integer(right_int))

    return arec, Interpreter(ObjectSpace())


def test_mul_primitive():
    arec, interp = setup_primitive_test(200, 100)

    _mul(None, arec, interp)

    value = arec.pop()
    assert value.get_integer_value() == 20000

def test_add_primitive():
    arec, interp = setup_primitive_test(200, 100)

    _add(None, arec, interp)

    value = arec.pop()
    assert value.get_integer_value() == 300

def test_sub_primitive():
    arec, interp = setup_primitive_test(200, 100)

    _sub(None, arec, interp)

    value = arec.pop()
    assert value.get_integer_value() == -100

def test_div_primitive():
    arec, interp = setup_primitive_test(50, 100)

    _div(None, arec, interp)

    value = arec.pop()
    assert(value.get_integer_value() == 2)

def test_mod_primitive():
    arec, interp = setup_primitive_test(3, 100)

    _mod(None, arec, interp)

    value = arec.pop()
    assert value.get_integer_value() == 1

def test_eq_primitive_true():
    arec, interp = setup_primitive_test(10, 10)

    _eq(None, arec, interp)

    value = arec.pop()
    assert isinstance(value, Boolean)
    assert value.get_boolean_value() == True

def test_eq_primitive_false():
    arec, interp = setup_primitive_test(11, 10)

    _eq(None, arec, interp)

    value = arec.pop()
    assert isinstance(value, Boolean)
    assert value.get_boolean_value() == False
