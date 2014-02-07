from wlvlang.compiler import ast
from wlvlang.compiler.context import MethodCompilerContext

from wlvlang.vm.vm_universe import VM_Universe
from wlvlang.interpreter.bytecode import Bytecode

from wlvlang.vmobjects.boolean import Boolean
from wlvlang.vmobjects.integer import Integer


def create_interpreter_context():
    universe = VM_Universe()
    ctx = MethodCompilerContext(universe)
    return ctx

def test_ast_integer_compile():
    ctx = create_interpreter_context()
    node = ast.IntegerConstant(100)
    node.compile(ctx)

    # Expect the constant to be stored in the literals area at position 0 (as this was a new context)
    assert ctx._literals[0] == Integer(100)

    # Expect the byte code to be [Bytecode.LOAD_CONST, 0]
    assert ctx.bytecode == [Bytecode.LOAD_CONST, chr(0)]

def test_ast_boolean_constant_compiler():
    ctx = create_interpreter_context()
    node = ast.BooleanConstant(True)
    node.compile(ctx)

    # Expect the constant to be stored in the literals area at position 0 (as this was a new context)
    assert ctx._literals[0] == Boolean(True)

    # Expect the byte code to be [Bytecode.LOAD_CONST, 0]
    assert ctx.bytecode == [Bytecode.LOAD_CONST, chr(0)]

def test_ast_assignment_compiler():
    ctx = create_interpreter_context()
    node = ast.Assignment('a', ast.BooleanConstant(True))
    node.compile(ctx)

    # Expect the constant to be stored in the literals area at position 0
    assert ctx._literals[0] == Boolean(True)

    # Expect the bytecode to be [Bytecode.LOAD_CONST, 0, Bytecode.STORE, 0]
    assert ctx.bytecode == [Bytecode.LOAD_CONST, chr(0), Bytecode.STORE, chr(0)]

def test_compile_function():
    universe = VM_Universe()
    interpreter = Interpreter(universe)

    root_context = MethodCompilerContext(universe)
    ast = parse("""a = 10 * 10
                print a""")

    ast.compile(root_context)
    root_context.bytecode.append(Bytecode.HALT)
    method = root_context.generate_method()
    arec = ActivationRecord(
        root_context._locals + root_context._literals,
        len(root_context._locals),
        len(root_context._literals),
        10,
        None,
        access_link=None)

    interpreter.interpret(method, arec)
    assert False

