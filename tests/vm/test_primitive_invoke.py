import pytest

from wlvlang.vm.vm_universe import VM_Universe
from wlvlang.interpreter.activationrecord import ActivationRecord

from wlvlang.vmobjects.boolean import Boolean


def test_primitive_invoke_integer():
    universe = VM_Universe()
    arec = ActivationRecord(2, None)

    integera = universe.new_integer(10)
    integerb = universe.new_integer(100)

    integera.send(arec, "_eq", [integerb], universe, None)
    value = arec.pop()
    assert(isinstance(value, Boolean))
    assert(value.get_value() == False)
