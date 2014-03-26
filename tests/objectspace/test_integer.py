import pytest

from wlvlang.interpreter.frame import Frame

from wlvlang.interpreter.objectspace.integer import Integer
from wlvlang.interpreter.objectspace.boolean import Boolean
from wlvlang.interpreter.objectspace.method import Method
from wlvlang.interpreter.objectspace.primitives.integer_primitive import _mul, _add, _div, _mod, _sub, _eq

from wlvlang.interpreter.interpreter import Interpreter
from wlvlang.interpreter.space import ObjectSpace

def test_get_value():
    subject = Integer(42)

    assert subject.get_integer_value() == 42

def setup_primitive_test(left_int, right_int):
    # Create an empty method object (it's not used in these tests)
    m = Method([], 0, [], 2)
    frame = Frame(previous_frame=None, method=m, access_link=None)

    frame.push(Integer(left_int))
    frame.push(Integer(right_int))

    return frame, ObjectSpace()


def test_mul_primitive():
    arec, space = setup_primitive_test(200, 100)

    _mul(arec, space)

    value = arec.pop()
    assert value.get_integer_value() == 20000

def test_add_primitive():
    arec, space = setup_primitive_test(200, 100)

    _add(arec, space)

    value = arec.pop()
    assert value.get_integer_value() == 300

def test_sub_primitive():
    arec, space = setup_primitive_test(200, 100)

    _sub(arec, space)

    value = arec.pop()
    assert value.get_integer_value() == -100

def test_div_primitive():
    arec, space = setup_primitive_test(50, 100)

    _div(arec, space)

    value = arec.pop()
    assert(value.get_integer_value() == 2)

def test_mod_primitive():
    arec, space = setup_primitive_test(3, 100)

    _mod(arec, space)

    value = arec.pop()
    assert value.get_integer_value() == 1

def test_eq_primitive_true():
    arec, space = setup_primitive_test(10, 10)

    _eq(arec, space)

    value = arec.pop()
    assert isinstance(value, Boolean)
    assert value.get_boolean_value() == True

def test_eq_primitive_false():
    arec, space = setup_primitive_test(11, 10)

    _eq(arec, space)

    value = arec.pop()
    assert isinstance(value, Boolean)
    assert value.get_boolean_value() == False
