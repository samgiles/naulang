import pytest

from wlvlang.interpreter.activationrecord import ActivationRecord
from wlvlang.vmobjects.integer import Integer
from wlvlang.vmobjects.primitives.integer_primitive import _mul, _add, _div

def test_get_value():
    subject = Integer(10)

    assert(subject.get_value() == 10)


def test_mul_primitive():

    arec = ActivationRecord(2, None)

    arec.push(Integer(100))
    arec.push(Integer(200))

    _mul(None, arec, None)

    value = arec.pop()
    assert(value.get_value() == 20000)

def test_add_primitive():
    arec = ActivationRecord(2, None)

    arec.push(Integer(100))
    arec.push(Integer(200))

    _add(None, arec, None)

    value = arec.pop()
    assert(value.get_value() == 300)

def test_div_primitive():
    arec = ActivationRecord(2, None)

    arec.push(Integer(100))
    arec.push(Integer(50))

    _div(None, arec, None)

    value = arec.pop()
    assert(value.get_value() == 2)

