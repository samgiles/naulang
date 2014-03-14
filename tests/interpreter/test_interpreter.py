
from wlvlang.interpreter.interpreter import Interpreter
from wlvlang.interpreter.activationrecord import  ActivationRecord
from wlvlang.interpreter.bytecode import Bytecode
from wlvlang.interpreter.space import ObjectSpace

from wlvlang.interpreter.objectspace.integer import Integer
from wlvlang.interpreter.objectspace.method import Method
from wlvlang.interpreter.objectspace.array import Array

from wlvlang.runtime.executioncontext import Task

def create_test_method(literals, locals, bytecode):
    """ create_test_method(literals, locals, bytecode) """
    return Method(literals, locals, bytecode, 20)

def create_frame(method, stack_size, parent=None, access_link=None):
    return ActivationRecord(stack_size, previous_record=parent, method=method, access_link=access_link)

def create_space_and_interpreter():
    space = ObjectSpace()
    return space, Interpreter(space)

def create_task(frame):
    task = Task()
    task.set_top_frame(frame)
    return task


def simple_setup(literals=[], locals=[], bytecode=[], stack_space=100):
    method = create_test_method(literals, locals, bytecode)
    frame = create_frame(method, stack_space)
    space, interpreter = create_space_and_interpreter()
    task = create_task(frame)
    return space, interpreter, task, frame

def test_bc_HALT():
    # TODO: Is this test needed? No assertions here, but I guess it's a little useful
    # to have in case this code starts failing
    _, interpreter, task, _ = simple_setup(bytecode=[Bytecode.HALT], stack_space=0)

    while interpreter.interpreter_step(task):
        pass

def test_bc_LOAD_CONST():
    """ Tests the 'LOAD_CONST n;' bytecode, where n is the offset in the literals' space to load

         Expected:
            Load a constant from the literals area of the frame on to the top of the stack
    """
    space, interpreter, task, frame = simple_setup(literals=[Integer(10)], locals=[None], bytecode=[Bytecode.LOAD_CONST, 0, Bytecode.HALT])

    while interpreter.interpreter_step(task):
        pass

    assert frame.peek() == space.new_integer(10)

def test_bc_LOAD():
    """ Tests the 'LOAD n;' bytecode, where n is the offset in the locals' space to load

        Expected:
            Load a local from the locals area of the frame
            on to the top of the stack
    """
    space, interpreter = create_space_and_interpreter()
    space, interpreter, task, frame = simple_setup(literals=[], locals=[None], bytecode=[Bytecode.LOAD, 0])

    frame.set_local_at(0, space.new_integer(10))
    interpreter.interpreter_step(task)

    assert frame.peek() == Integer(10)
    assert frame.get_pc() == 2

def test_bc_STORE():
    """ Tests the 'STORE n;' bytecode where n is the offset in the locals'
             space to store the value at the top of the stack to.

        Expected:
            Store the local on top of the stack in it's respective position
    """
    space, interpreter, task, frame = simple_setup(literals=[], locals=[None], bytecode=[Bytecode.STORE, 0])
    frame.push(space.new_integer(100))
    interpreter.interpreter_step(task)

    assert frame.get_local_at(0) == Integer(100)
    assert frame.get_pc() == 2

def test_bc_MUL():
    """ Tests the 'MUL;' bytecode

        Expected:
            Store a result of a multiply operation on top of the stack using the values on the stack as arguments (uses the primitive operations)
    """

    space, interpreter, task, frame = simple_setup(literals=[], locals=[None], bytecode=[Bytecode.MUL])
    frame.push(space.new_integer(100))
    frame.push(space.new_integer(30))
    interpreter.interpreter_step(task)

    assert frame.peek() == Integer(3000)
    assert frame.get_pc() == 1

def test_bc_ARRAY_STORE():
    """  Tests the 'ARRAY_STORE;' bytecode which takes three values from the stack,
            the top value it pops off is the value it will place into the array,
            the next value is the index in the array
            and finally the, the last value is the array object
    Expected:
        Store the top of the stack into the index specified in top_of_stack - 1, in
        the array object found at top_of_stack - 2

    """

    space, interpreter, task, frame = simple_setup(literals=[], locals=[], bytecode=[Bytecode.ARRAY_STORE])

    array = space.new_array(10)
    frame.push(array)
    frame.push(space.new_integer(0))
    frame.push(space.new_integer(100))
    interpreter.interpreter_step(task)

    assert array.get_value_at(0) == Integer(100)
    assert frame.get_pc() == 1

def test_bc_ARRAY_LOAD():
    """ Tests the 'ARRAY_LOAD;' bytecode which takes two values from the stack,
            the top value is the index to access
            the next value on the stack is the array
        Expected:
            Put the value in the array (top_of_stack - 2) at the index (top_of_stack - 1) on top
            of the stack.
    """

    space, interpreter, task, frame = simple_setup(literals=[], locals=[], bytecode=[Bytecode.ARRAY_LOAD])

    array = space.new_array(10)
    array.set_value_at(0, space.new_integer(900))
    frame.push(array)
    frame.push(space.new_integer(0))
    interpreter.interpreter_step(task)

    assert frame.peek() == Integer(900)
    assert frame.get_pc() == 1

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

    frame = create_frame(method, 5)
    task = create_task(frame)

    while interpreter.interpreter_step(task):
        pass

    stack_top = frame.peek()
    print repr(stack_top)
    assert stack_top == Integer(100)


def test_bc_GREATER_THAN_EQ():
    space, interpreter = create_space_and_interpreter()
    method = create_test_method([], [], [Bytecode.GREATER_THAN_EQ, Bytecode.HALT])
    frame = create_frame(method, 2)
    frame.push(space.new_integer(10))
    frame.push(space.new_integer(20))
    interpreter.interpret(method, frame)

    assert frame.peek() == space.new_boolean(False)

    frame = create_frame(method, 2)
    frame.push(space.new_integer(20))
    frame.push(space.new_integer(20))
    interpreter.interpret(method, frame)

    assert frame.peek() == space.new_boolean(True)

    frame = create_frame(method, 2)
    frame.push(space.new_integer(30))
    frame.push(space.new_integer(20))
    interpreter.interpret(method, frame)

    assert frame.peek() == space.new_boolean(True)

def test_bc_INVOKE_GLOBAL():
    space, interpreter = create_space_and_interpreter()
    method = create_test_method([], [], [Bytecode.INVOKE_GLOBAL, 0, Bytecode.HALT])

    frame = create_frame(method, 3)
    frame.push(space.new_integer(10))

    interpreter.interpret(method, frame)

    assert isinstance(frame.peek(), Array)

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

    import pytest;pytest.set_trace()
    task = create_task(None)
    mainmethod.invoke(task)

    last_active_frame = task.get_top_frame();
    while interpreter.interpreter_step(task):
        has_task_finished = task.get_top_frame() is None
        if has_task_finished:
            break

        last_active_frame = task.get_top_frame()

    assert last_active_frame.peek() == Integer(10)
