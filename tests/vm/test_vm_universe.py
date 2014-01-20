import pytest

from wlvlang.vm.vm_universe import VM_Universe
from wlvlang.vmobjects.integer import Integer
from wlvlang.vmobjects.classs import Class


def test_new_integer():
    subject = VM_Universe()

    integer = subject.new_integer(10)
    assert(isinstance(integer, Integer))
    assert(integer.get_value() == 10)

def test_new_integer_class():
    subject = VM_Universe()
    integer = subject.new_integer(10)
    assert(isinstance(integer.get_class(subject), Class))
    assert(integer.get_class(subject) == subject.integerClass)
