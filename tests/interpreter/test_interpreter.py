
from naulang.interpreter.interpreter import Interpreter
from naulang.interpreter.frame import Frame
from naulang.interpreter.bytecode import Bytecode
from naulang.interpreter.space import ObjectSpace

from naulang.interpreter.objectspace.integer import Integer
from naulang.interpreter.objectspace.method import Method
from naulang.interpreter.objectspace.array import Array

from naulang.runtime.executioncontext import Task


def create_test_method(literals, locals, bytecode):
    """ create_test_method(literals, locals, bytecode) """
    return Method(literals, locals, bytecode, 20)


def create_frame(method, parent=None, access_link=None):
    return Frame(previous_frame=parent, method=method, access_link=access_link)


def create_space_and_interpreter():
    space = ObjectSpace()
    return space, Interpreter(space)


def create_task(frame):
    task = Task(None)
    task.set_top_frame(frame)
    return task


def simple_setup(literals=[], locals=0, bytecode=[]):
    method = create_test_method(literals, locals, bytecode)
    frame = create_frame(method)
    space, interpreter = create_space_and_interpreter()
    task = create_task(frame)
    return space, interpreter, task, frame


def _interpreter_step(interpreter, task):
    pc = task.get_top_frame().get_pc()
    method = task.get_current_method()
    frame = task.get_top_frame()
    return interpreter.interpreter_step(pc, method, frame, task)


def test_bc_HALT():
    # TODO: Is this test needed? No assertions here, but I guess it's a little useful
    # to have in case this code starts failing
    _, interpreter, task, _ = simple_setup(bytecode=[Bytecode.HALT])

    while _interpreter_step(interpreter, task):
        pass


def test_bc_RETURN():
    _, interpreter, task, frame = simple_setup(
        literals=[Integer(10)], bytecode=[Bytecode.LOAD_CONST, 0, Bytecode.RETURN])

    parent_method = create_test_method([], 0, [Bytecode.HALT])
    parent_frame = create_frame(parent_method)
    frame.set_previous_frame(parent_frame)

    while _interpreter_step(interpreter, task):
        pass

    assert parent_frame.peek() == Integer(10)


def test_bc_LOAD_CONST():
    """ Tests the 'LOAD_CONST n;' bytecode, where n is the offset in the literals' space to load

         Expected:
            Load a constant from the literals area of the frame on to the top of the stack
    """
    space, interpreter, task, frame = simple_setup(
        literals=[Integer(10)], locals=1, bytecode=[Bytecode.LOAD_CONST, 0, Bytecode.HALT])

    while _interpreter_step(interpreter, task):
        pass

    assert frame.peek() == space.new_integer(10)


def test_bc_LOAD():
    """ Tests the 'LOAD n;' bytecode, where n is the offset in the locals' space to load

        Expected:
            Load a local from the locals area of the frame
            on to the top of the stack
    """
    space, interpreter = create_space_and_interpreter()
    space, interpreter, task, frame = simple_setup(literals=[], locals=1, bytecode=[Bytecode.LOAD, 0])

    frame.set_local_at(0, space.new_integer(10))
    _interpreter_step(interpreter, task)

    assert frame.peek() == Integer(10)
    assert frame.get_pc() == 2


def test_bc_STORE():
    """ Tests the 'STORE n;' bytecode where n is the offset in the locals'
             space to store the value at the top of the stack to.

        Expected:
            Store the local on top of the stack in it's respective position
    """
    space, interpreter, task, frame = simple_setup(literals=[], locals=1, bytecode=[Bytecode.STORE, 0])
    frame.push(space.new_integer(100))
    _interpreter_step(interpreter, task)

    assert frame.get_local_at(0) == Integer(100)
    assert frame.get_pc() == 2


def test_bc_MUL():
    """ Tests the 'MUL;' bytecode

        Expected:
            Store a result of a multiply operation on top of the stack using
            the values on the stack as arguments (uses the primitive operations)
    """

    space, interpreter, task, frame = simple_setup(literals=[], locals=1, bytecode=[Bytecode.MUL])
    frame.push(space.new_integer(100))
    frame.push(space.new_integer(30))
    _interpreter_step(interpreter, task)

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

    space, interpreter, task, frame = simple_setup(literals=[], locals=0, bytecode=[Bytecode.ARRAY_STORE])

    array = space.new_array(10)
    frame.push(array)
    frame.push(space.new_integer(0))
    frame.push(space.new_integer(100))
    _interpreter_step(interpreter, task)

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

    space, interpreter, task, frame = simple_setup(literals=[], locals=0, bytecode=[Bytecode.ARRAY_LOAD])

    array = space.new_array(10)
    array.set_value_at(0, space.new_integer(900))
    frame.push(array)
    frame.push(space.new_integer(0))
    _interpreter_step(interpreter, task)

    assert frame.peek() == Integer(900)
    assert frame.get_pc() == 1


def test_bc_LOAD_DYNAMIC():
    space, interpreter = create_space_and_interpreter()
    outer_integer = space.new_integer(100)
    method = create_test_method(literals=[
        outer_integer,
        create_test_method([], 0, [
            Bytecode.LOAD_DYNAMIC, 0, 1,
            Bytecode.RETURN,
            Bytecode.HALT
        ])
    ],
        locals=2,
        bytecode=[
            Bytecode.LOAD_CONST, 0,
            Bytecode.STORE, 0,
            Bytecode.LOAD_CONST, 1,
            Bytecode.STORE, 1,
            Bytecode.LOAD, 1,
            Bytecode.INVOKE,
            Bytecode.HALT
        ])

    frame = create_frame(method)
    task = create_task(frame)

    while _interpreter_step(interpreter, task):
        pass

    stack_top = frame.peek()
    print repr(stack_top)
    assert stack_top == Integer(100)


def test_bc_GREATER_THAN_EQ():
    """ Tests the 'GREATER_THAN_EQ;' bytecode
        Expected:
            The values on top of the stack should be compared and a boolean should be
            placed on top of the stack
    """
    space, interpreter, task, frame = simple_setup(literals=[], locals=0, bytecode=[Bytecode.GREATER_THAN_EQ, 0])

    frame.push(space.new_integer(10))
    frame.push(space.new_integer(20))
    _interpreter_step(interpreter, task)

    print repr(frame.peek())
    print repr(frame.peek().get_as_string())
    assert frame.pop() == space.new_boolean(False)

    frame.push(space.new_integer(20))
    frame.push(space.new_integer(20))
    frame.set_pc(0)
    _interpreter_step(interpreter, task)

    assert frame.pop() == space.new_boolean(True)

    frame.push(space.new_integer(30))
    frame.push(space.new_integer(20))
    frame.set_pc(0)
    _interpreter_step(interpreter, task)

    assert frame.pop() == space.new_boolean(True)


def test_bc_LESS_THAN():
    """ Tests the 'LESS_THAN;' bytecode
        Expected:
            The values on top of the stack should be compared and a boolean should be
            placed on top of the stack
    """
    space, interpreter, task, frame = simple_setup(literals=[], locals=0, bytecode=[Bytecode.LESS_THAN, 0])

    frame.push(space.new_integer(20))
    frame.push(space.new_integer(10))
    _interpreter_step(interpreter, task)

    assert frame.pop() == space.new_boolean(False)

    frame.push(space.new_integer(20))
    frame.push(space.new_integer(20))
    frame.set_pc(0)
    _interpreter_step(interpreter, task)

    assert frame.pop() == space.new_boolean(False)

    frame.push(space.new_integer(10))
    frame.push(space.new_integer(20))
    frame.set_pc(0)
    _interpreter_step(interpreter, task)

    assert frame.pop() == space.new_boolean(True)


def test_bc_GREATER_THAN():
    """ Tests the 'GREATER_THAN;' bytecode
        Expected:
            The values on top of the stack should be compared and a boolean should be
            placed on top of the stack
    """
    space, interpreter, task, frame = simple_setup(literals=[], locals=0, bytecode=[Bytecode.GREATER_THAN, 0])

    frame.push(space.new_integer(20))
    frame.push(space.new_integer(10))
    _interpreter_step(interpreter, task)

    assert frame.pop() == space.new_boolean(True)

    frame.push(space.new_integer(20))
    frame.push(space.new_integer(20))
    frame.set_pc(0)
    _interpreter_step(interpreter, task)

    assert frame.pop() == space.new_boolean(False)

    frame.push(space.new_integer(10))
    frame.push(space.new_integer(20))
    frame.set_pc(0)
    _interpreter_step(interpreter, task)

    assert frame.pop() == space.new_boolean(False)


def test_bc_INVOKE_GLOBAL():
    """ Tests the 'INVOKE_GLOBAL n;' expect the global method identified by n to be executed
        Expected:
            Put an array sized by the value on top of the stack onto the top of the stack
    """
    space, interpreter, task, frame = simple_setup(literals=[], locals=0, bytecode=[Bytecode.INVOKE_GLOBAL, 0])
    frame.push(space.new_integer(10))

    _interpreter_step(interpreter, task)

    assert isinstance(frame.peek(), Array)


def test_bc_INVOKE():
    space, interpreter = create_space_and_interpreter()
    innerMethod = Method([], 1, [
        Bytecode.LOAD, 0,
        Bytecode.LOAD_DYNAMIC, 0, 1,
        Bytecode.MUL,
        Bytecode.RETURN,
        Bytecode.HALT
    ], 2, argument_count=1)

    method = Method([innerMethod], 1, [
        Bytecode.LOAD_CONST, 0,
        Bytecode.RETURN,
        Bytecode.HALT
    ], 1, argument_count=1)

    mainmethod = Method([method, Integer(2), Integer(3), Integer(10)], 3, [
        Bytecode.LOAD_CONST, 0,
        Bytecode.STORE, 0,
        Bytecode.LOAD_CONST, 1,
        Bytecode.LOAD, 0,
        Bytecode.INVOKE,
        Bytecode.STORE, 1,
        Bytecode.LOAD_CONST, 2,
        Bytecode.LOAD, 0,
        Bytecode.INVOKE,
        Bytecode.STORE, 2,
        Bytecode.LOAD_CONST, 3,
        Bytecode.LOAD, 1,
        Bytecode.INVOKE,
        Bytecode.LOAD_CONST, 3,
        Bytecode.LOAD, 2,
        Bytecode.INVOKE,
        Bytecode.SUB,
        Bytecode.RETURN,
        Bytecode.HALT
    ], 10, argument_count=0)

    task = create_task(None)
    mainmethod.invoke(task.get_top_frame(), task)

    last_active_frame = task.get_top_frame()
    while _interpreter_step(interpreter, task):
        has_task_finished = task.get_top_frame() is None
        if has_task_finished:
            break

        last_active_frame = task.get_top_frame()

    assert last_active_frame.peek() == Integer(10)
