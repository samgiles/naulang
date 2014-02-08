import pytest

from wlvlang.interpreter.interpreter import Interpreter
from wlvlang.interpreter.bytecode import Bytecode
from wlvlang.vm.vm_universe import VM_Universe
from wlvlang.vmobjects.integer import Integer

def create_test_method(literals, locals, bytecode):
    from wlvlang.vmobjects.method import Method
    return Method(literals, locals, bytecode)

def create_arec(method, temp_space, parent=None):
    from wlvlang.interpreter.activationrecord import ActivationRecord
    return ActivationRecord(method._locals + method._literals, len(method._locals), len(method._literals), temp_space, parent)

def create_universe_and_interpreter():
    vm_universe = VM_Universe()
    return vm_universe, Interpreter(vm_universe)

def test_bc_HALT():
    method = create_test_method([], [], [Bytecode.HALT])
    arec = create_arec(method, 0)
    _, interpreter = create_universe_and_interpreter()

    kontinue, new_pc = interpreter.interpreter_step(0, method, arec)
    assert kontinue == False
    assert new_pc == 0

def test_bc_LOAD_CONST():
    """ Expected:
            Load a constant from the literals area of the ActivationRecord
            on to the top of the stack
    """
    uv, interpreter = create_universe_and_interpreter()
    method = create_test_method([uv.new_integer(10)], [None], [Bytecode.LOAD_CONST, chr(0)])
    arec = create_arec(method, 1)

    kontinue, new_pc = interpreter.interpreter_step(0, method, arec)

    assert kontinue
    assert new_pc == 2
    assert arec.pop() == Integer(10)

def test_bc_LOAD():
    """ Expected:
            Load a local from the locals area of the ActivationRecord
            on to the top of the stack
    """
    uv, interpreter = create_universe_and_interpreter()
    method = create_test_method([], [uv.new_integer(10)], [Bytecode.LOAD, chr(0)])
    arec = create_arec(method, 1)
    kontinue, new_pc = interpreter.interpreter_step(0, method, arec)

    assert kontinue
    assert new_pc == 2
    assert arec.pop() == Integer(10)

def test_bc_STORE():
    """ Expected:
            Store the local on top of the stack in it's respective
            position
    """
    uv, interpreter = create_universe_and_interpreter()
    method = create_test_method([], [None], [Bytecode.STORE, chr(0)])
    arec = create_arec(method, 1)
    arec.push(uv.new_integer(100))
    kontinue, new_pc = interpreter.interpreter_step(0, method, arec)

    assert kontinue
    assert new_pc == 2
    assert arec.get_local_at(0) == Integer(100)
