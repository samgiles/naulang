import pytest

from wlvlang.interpreter.interpreter import Interpreter
from wlvlang.interpreter.activationrecord import  ActivationRecord
from wlvlang.interpreter.bytecode import Bytecode
from wlvlang.interpreter.space import ObjectSpace
from wlvlang.interpreter.objectspace.integer import Integer
from wlvlang.interpreter.objectspace.boolean import Boolean
from wlvlang.interpreter.objectspace.method import Method
from wlvlang.interpreter.objectspace.array import Array

def create_test_method(literals, locals, bytecode):
    """ create_test_method(literals, locals, bytecode) """
    return Method(literals, locals, bytecode, 20)

def create_arec(method, temp_space, parent=None, access_link=None):
    from wlvlang.interpreter.activationrecord import ActivationRecord
    return ActivationRecord(method.locals, method.literals, temp_space, parent, access_link)

def create_space_and_interpreter():
    space = ObjectSpace()
    return space, Interpreter(space)

def test_bc_HALT():
    method = create_test_method([], [], [Bytecode.HALT])
    arec = create_arec(method, 0)
    _, interpreter = create_space_and_interpreter()

    interpreter.interpret(method, arec)
    # TODO: Is this needed? No assertions here, but I guess it's a little useful
    # to have if this code starts failing

def test_bc_LOAD_CONST():
    """ Expected:
            Load a constant from the literals area of the ActivationRecord
            on to the top of the stack
    """
    space, interpreter = create_space_and_interpreter()
    method = create_test_method([space.new_integer(10)], [None], [Bytecode.LOAD_CONST, 0, Bytecode.HALT])
    arec = create_arec(method, 1)

    interpreter.interpret(method, arec)

    assert arec.pop() == Integer(10)

def test_bc_LOAD():
    """ Expected:
            Load a local from the locals area of the ActivationRecord
            on to the top of the stack
    """
    space, interpreter = create_space_and_interpreter()
    method = create_test_method([], [space.new_integer(10)], [Bytecode.LOAD, 0, Bytecode.HALT])
    arec = create_arec(method, 1)
    interpreter.interpret(method, arec)
    assert arec.pop() == Integer(10)

def test_bc_STORE():
    """ Expected:
            Store the local on top of the stack in it's respective
            position
    """
    space, interpreter = create_space_and_interpreter()
    method = create_test_method([], [None], [Bytecode.STORE, 0, Bytecode.HALT])
    arec = create_arec(method, 1)
    arec.push(space.new_integer(100))
    interpreter.interpret(method, arec)

    assert arec.get_local_at(0) == Integer(100)

def test_bc_MUL():
    """ Expected:
            Store a result of a multiply operation on top of the stack using the values on the stack as arguments (uses the primitive operations)

        As these operations depend on the types they are being performed
        on the objectspace handles the result of these operations.
        testing one for now is sufficient that the _send operation is
        sent correctly
    """

    space, interpreter = create_space_and_interpreter()
    method = create_test_method([], [], [Bytecode.MUL, Bytecode.HALT])
    arec = create_arec(method, 2)
    arec.push(space.new_integer(100))
    arec.push(space.new_integer(30))
    interpreter.interpret(method, arec)

    assert arec.peek() == Integer(3000)

def test_bc_ARRAY_STORE():
    """ Expected:

    """
    space, interpreter = create_space_and_interpreter()
    method = create_test_method([], [], [Bytecode.ARRAY_STORE, Bytecode.HALT])
    arec = create_arec(method, 4)

    array = space.new_array(10)
    arec.push(array)
    arec.push(space.new_integer(0))
    arec.push(space.new_integer(100))
    interpreter.interpret(method, arec)

    assert array.get_value_at(0) == Integer(100)

def test_bc_ARRAY_LOAD():
    """ Expected:
    """

    space, interpreter = create_space_and_interpreter()
    method = create_test_method([], [], [Bytecode.ARRAY_LOAD, Bytecode.HALT])
    arec = create_arec(method, 4)

    array = space.new_array(10)
    array.set_value_at(0, space.new_integer(900))
    arec.push(array)
    arec.push(space.new_integer(0))
    interpreter.interpret(method, arec)

def test_bc_LOAD_DYNAMIC():
    space, interpreter = create_space_and_interpreter()
    outer_integer = space.new_integer(100)
    method = create_test_method([
        outer_integer,
        create_test_method([], [], [
                Bytecode.LOAD_DYNAMIC, 0, 1,
                Bytecode.RETURN,
                Bytecode.HALT
            ])
    ],
    [None, None],
    [
        Bytecode.LOAD_CONST, 0,
        Bytecode.STORE, 0,
        Bytecode.LOAD_CONST, 1,
        Bytecode.STORE, 1,
        Bytecode.INVOKE, 1,
        Bytecode.HALT
    ])

    arec = create_arec(method, 5)

    interpreter.interpret(method, arec)

    stack_top = arec.peek()
    print repr(stack_top)
    assert stack_top == Integer(100)


def test_bc_GREATER_THAN_EQ():
    space, interpreter = create_space_and_interpreter()
    method = create_test_method([], [], [Bytecode.GREATER_THAN_EQ, Bytecode.HALT])
    arec = create_arec(method, 2)
    arec.push(space.new_integer(10))
    arec.push(space.new_integer(20))
    interpreter.interpret(method, arec)

    assert arec.peek() == space.new_boolean(False)

    arec = create_arec(method, 2)
    arec.push(space.new_integer(20))
    arec.push(space.new_integer(20))
    interpreter.interpret(method, arec)

    assert arec.peek() == space.new_boolean(True)

    arec = create_arec(method, 2)
    arec.push(space.new_integer(30))
    arec.push(space.new_integer(20))
    interpreter.interpret(method, arec)

    assert arec.peek() == space.new_boolean(True)

def test_bc_INVOKE_GLOBAL():
    space, interpreter = create_space_and_interpreter()
    method = create_test_method([], [], [Bytecode.INVOKE_GLOBAL, 0, Bytecode.HALT])

    arec = create_arec(method, 3)
    arec.push(space.new_integer(10))

    interpreter.interpret(method, arec)

    assert isinstance(arec.peek(), Array)

def test_bc_INVOKE():
    space, interpreter = create_space_and_interpreter()
    innerMethod = Method([], [None], [
        Bytecode.LOAD, 0,
        Bytecode.LOAD_DYNAMIC, 0, 1,
        Bytecode.MUL,
        Bytecode.RETURN,
        Bytecode.HALT
    ], 2, argument_count=1)

    method = Method([innerMethod], [None], [
        Bytecode.LOAD_CONST, 0,
        Bytecode.RETURN,
        Bytecode.HALT
    ], 1, argument_count=1)

    mainmethod = Method([method, Integer(2), Integer(3), Integer(10)], [None, None, None], [
        Bytecode.LOAD_CONST, 0,
        Bytecode.STORE, 0,
        Bytecode.LOAD_CONST, 1,
        Bytecode.INVOKE, 0,
        Bytecode.STORE, 1,
        Bytecode.LOAD_CONST, 2,
        Bytecode.INVOKE, 0,
        Bytecode.STORE, 2,
        Bytecode.LOAD_CONST, 3,
        Bytecode.INVOKE, 1,
        Bytecode.LOAD_CONST, 3,
        Bytecode.INVOKE, 2,
        Bytecode.SUB,
        Bytecode.RETURN,
        Bytecode.HALT
    ], 10, argument_count=0)

    arec = ActivationRecord([None], [], 5, None)
    mainmethod.invoke(arec, interpreter)
    assert arec.peek() == Integer(10)
