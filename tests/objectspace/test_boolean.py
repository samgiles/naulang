from naulang.interpreter.frame import Frame
from naulang.interpreter.space import ObjectSpace

from naulang.interpreter.objectspace.method import Method
from naulang.interpreter.objectspace.boolean import Boolean


def test_get_value():
    subjecta = Boolean(True)
    subjectb = Boolean(False)

    assert subjecta.get_boolean_value()
    assert not subjectb.get_boolean_value()


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
    assert value.get_boolean_value()


def test_eq_primitive_true_false():
    arec, space = setup_primitive_test(True, False)

    arec.peek().w_eq(arec, space)

    value = arec.pop()
    assert not value.get_boolean_value()


def test_eq_primitive_false_true():
    arec, space = setup_primitive_test(False, True)

    arec.peek().w_eq(arec, space)

    value = arec.pop()
    assert not value.get_boolean_value()


def test_or_primitive_true_true():
    arec, space = setup_primitive_test(True, True)

    arec.peek().w_or(arec, space)

    value = arec.pop()
    assert value.get_boolean_value()


def test_or_primitive_true_false():
    arec, space = setup_primitive_test(True, False)

    arec.peek().w_or(arec, space)

    value = arec.pop()
    assert value.get_boolean_value()


def test_or_primitive_false_true():
    arec, space = setup_primitive_test(False, True)

    arec.peek().w_or(arec, space)

    value = arec.pop()
    assert value.get_boolean_value()


def test_or_primitive_false_false():
    arec, space = setup_primitive_test(False, False)

    arec.peek().w_or(arec, space)

    value = arec.pop()
    assert not value.get_boolean_value()


def test_and_primitive_true_true():
    arec, space = setup_primitive_test(True, True)

    arec.peek().w_and(arec, space)

    value = arec.pop()
    assert value.get_boolean_value()


def test_and_primitive_false_true():
    arec, space = setup_primitive_test(False, True)

    arec.peek().w_and(arec, space)
    value = arec.pop()
    assert not value.get_boolean_value()
