from wlvlang.interpreter.activationrecord import ActivationRecord
from wlvlang.interpreter.interpreter import Interpreter
from wlvlang.interpreter.space import ObjectSpace

from wlvlang.interpreter.objectspace.method import Method
from wlvlang.interpreter.objectspace.boolean import Boolean

from wlvlang.interpreter.objectspace.primitives.boolean_primitive import _eq, _or, _and

def test_get_value():
    subjecta = Boolean(True)
    subjectb = Boolean(False)

    assert subjecta.get_boolean_value() == True
    assert subjectb.get_boolean_value() == False

def setup_primitive_test(left_val, right_val):
    # Create an empty method object (it's not used in these tests)
    m = Method([], 0, [], 2)
    arec = ActivationRecord(previous_record=None, method=m, access_link=None)

    arec.push(Boolean(left_val))
    arec.push(Boolean(right_val))

    return arec, Interpreter(ObjectSpace())

def test_eq_primitive_true_true():
    arec, interp = setup_primitive_test(True, True)

    _eq(None, arec, interp)

    value = arec.pop()
    assert value.get_boolean_value() == True

def test_eq_primitive_true_false():
    arec, interp = setup_primitive_test(True, False)

    _eq(None, arec, interp)

    value = arec.pop()
    assert value.get_boolean_value() == False

def test_eq_primitive_false_true():
    arec, interp = setup_primitive_test(False, True)

    _eq(None, arec, interp)

    value = arec.pop()
    assert value.get_boolean_value() == False

def test_or_primitive_true_true():
    arec, interp = setup_primitive_test(True, True)

    _or(None, arec, interp)

    value = arec.pop()
    assert value.get_boolean_value() == True

def test_or_primitive_true_false():
    arec, interp = setup_primitive_test(True, False)

    _or(None, arec, interp)

    value = arec.pop()
    assert value.get_boolean_value() == True

def test_or_primitive_false_true():
    arec, interp = setup_primitive_test(False, True)

    _or(None, arec, interp)

    value = arec.pop()
    assert value.get_boolean_value() == True

def test_or_primitive_false_false():
    arec, interp = setup_primitive_test(False, False)

    _or(None, arec, interp)

    value = arec.pop()
    assert value.get_boolean_value() == False

def test_and_primitive_true_true():
    arec, interp = setup_primitive_test(True, True)

    _and(None, arec, interp)

    value = arec.pop()
    assert value.get_boolean_value() == True

def test_and_primitive_false_true():
    arec, interp = setup_primitive_test(False, True)

    _and(None, arec, interp)
    value = arec.pop()
    assert value.get_boolean_value() == False
