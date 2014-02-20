import pytest

from wlvlang.interpreter.interpreter import Interpreter
from wlvlang.interpreter.bytecode import Bytecode
from wlvlang.vm.vm_universe import VM_Universe
from wlvlang.vmobjects.integer import Integer
from wlvlang.vmobjects.boolean import Boolean

def create_test_method(literals, locals, bytecode):
    """ create_test_method(literals, locals, bytecode) """
    from wlvlang.vmobjects.method import Method
    return Method(None, literals, locals, bytecode)

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

    interpreter.interpret(method, arec)
    # TODO: Is this needed? No assertions here, but I guess it's a little useful
    # to have if this code starts failing

def test_bc_LOAD_CONST():
    """ Expected:
            Load a constant from the literals area of the ActivationRecord
            on to the top of the stack
    """
    uv, interpreter = create_universe_and_interpreter()
    method = create_test_method([uv.new_integer(10)], [None], [Bytecode.LOAD_CONST, chr(0), Bytecode.HALT])
    arec = create_arec(method, 1)

    interpreter.interpret(method, arec)

    assert arec.pop() == Integer(10)

def test_bc_LOAD():
    """ Expected:
            Load a local from the locals area of the ActivationRecord
            on to the top of the stack
    """
    uv, interpreter = create_universe_and_interpreter()
    method = create_test_method([], [uv.new_integer(10)], [Bytecode.LOAD, chr(0), Bytecode.HALT])
    arec = create_arec(method, 1)
    interpreter.interpret(method, arec)
    assert arec.pop() == Integer(10)

def test_bc_STORE():
    """ Expected:
            Store the local on top of the stack in it's respective
            position
    """
    uv, interpreter = create_universe_and_interpreter()
    method = create_test_method([], [None], [Bytecode.STORE, chr(0), Bytecode.HALT])
    arec = create_arec(method, 1)
    arec.push(uv.new_integer(100))
    interpreter.interpret(method, arec)

    assert arec.get_local_at(0) == Integer(100)

def test_bc_MUL():
    """ Expected:
            Store a result of a multiply operation on top of the stack using the values on the stack as arguments (uses the primitive operations)

        As these operations depend on the types they are being performed
        on the vmobjects handle the result of these operations.
        testing one for now is sufficient that the _send operation is
        sent correctly
    """

    uv, interpreter = create_universe_and_interpreter()
    method = create_test_method([], [], [Bytecode.MUL, Bytecode.HALT])
    arec = create_arec(method, 2)
    arec.push(uv.new_integer(30))
    arec.push(uv.new_integer(100))
    interpreter.interpret(method, arec)

    assert arec.peek() == Integer(3000)

def test_bc_ARRAY_STORE():
    """ Expected:

    """
    uv, interpreter = create_universe_and_interpreter()
    method = create_test_method([], [], [Bytecode.ARRAY_STORE, Bytecode.HALT])
    arec = create_arec(method, 4)

    array = uv.new_array(10)
    arec.push(array)
    arec.push(uv.new_integer(0))
    arec.push(uv.new_integer(100))
    interpreter.interpret(method, arec)

    assert array.get_value_at(0) == Integer(100)

def test_bc_ARRAY_LOAD():
    """ Expected:
    """

    uv, interpreter = create_universe_and_interpreter()
    method = create_test_method([], [], [Bytecode.ARRAY_LOAD, Bytecode.HALT])
    arec = create_arec(method, 4)

    array = uv.new_array(10)
    array.set_value_at(0, uv.new_integer(900))
    arec.push(array)
    arec.push(uv.new_integer(0))
    interpreter.interpret(method, arec)

def test_bc_LOAD_DYNAMIC():
    uv, interpreter = create_universe_and_interpreter()
    outer_integer = Integer(100)
    method = create_test_method([
        outer_integer,
        create_test_method([], [], [
                Bytecode.LOAD_DYNAMIC, chr(0), chr(1),
                Bytecode.RETURN,
                Bytecode.HALT
            ])
    ],
    [None, None],
    [
        Bytecode.LOAD_CONST, chr(0),
        Bytecode.STORE, chr(0),
        Bytecode.LOAD_CONST, chr(1),
        Bytecode.STORE, chr(1),
        Bytecode.INVOKE, chr(1),
        Bytecode.HALT
    ])

    arec = create_arec(method, 5)

    interpreter.interpret(method, arec)

    stack_top = arec.peek()
    print repr(stack_top)
    assert stack_top == Integer(100)
