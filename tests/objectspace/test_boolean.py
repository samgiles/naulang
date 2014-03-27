from wlvlang.interpreter.frame import Frame
from wlvlang.interpreter.interpreter import Interpreter
from wlvlang.interpreter.space import ObjectSpace

from wlvlang.interpreter.objectspace.method import Method
from wlvlang.interpreter.objectspace.boolean import Boolean

def test_get_value():
    subjecta = Boolean(True)
    subjectb = Boolean(False)

    assert subjecta.get_boolean_value() == True
    assert subjectb.get_boolean_value() == False

def setup_primitive_test(left_val, right_val):
    # Create an empty method object (it's not used in these tests)
    m = Method([], 0, [], 2)
    arec = Frame(previous_frame=None, method=m, access_link=None)

    arec.push(Boolean(left_val))
    arec.push(Boolean(right_val))

    return arec, ObjectSpace()

def test_eq_primitive_true_true():
    arec, space = setup_primitive_test(True, True)
    arec.peek().w_eq(arec, space)

    value = arec.pop()
    assert value.get_boolean_value() == True

def test_eq_primitive_true_false():
    arec, space = setup_primitive_test(True, False)

    arec.peek().w_eq(arec, space)

    value = arec.pop()
    assert value.get_boolean_value() == False

def test_eq_primitive_false_true():
    arec, space = setup_primitive_test(False, True)

    arec.peek().w_eq(arec, space)

    value = arec.pop()
    assert value.get_boolean_value() == False

def test_or_primitive_true_true():
    arec, space = setup_primitive_test(True, True)

    arec.peek().w_or(arec, space)

    value = arec.pop()
    assert value.get_boolean_value() == True

def test_or_primitive_true_false():
    arec, space = setup_primitive_test(True, False)

    arec.peek().w_or(arec, space)

    value = arec.pop()
    assert value.get_boolean_value() == True

def test_or_primitive_false_true():
    arec, space = setup_primitive_test(False, True)

    arec.peek().w_or(arec, space)

    value = arec.pop()
    assert value.get_boolean_value() == True

def test_or_primitive_false_false():
    arec, space = setup_primitive_test(False, False)

    arec.peek().w_or(arec, space)

    value = arec.pop()
    assert value.get_boolean_value() == False

def test_and_primitive_true_true():
    arec, space = setup_primitive_test(True, True)

    arec.peek().w_and(arec, space)

    value = arec.pop()
    assert value.get_boolean_value() == True

def test_and_primitive_false_true():
    arec, space = setup_primitive_test(False, True)

    arec.peek().w_and(arec, space)
    value = arec.pop()
    assert value.get_boolean_value() == False
