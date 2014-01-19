import pytest

from wlvlang.vm.vm_universe import VM_Universe
from wlvlang.vmobjects.integer import Integer


def test_new_integer():
    subject = VM_Universe()

    integer = subject.new_integer(10)
    assert(isinstance(integer, Integer))
    assert(integer.get_value() == 10)
