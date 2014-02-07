from wlvlang.compiler import ast
from wlvlang.compiler.context import MethodCompilerContext

from wlvlang.vm.vm_universe import VM_Universe
from wlvlang.interpreter.bytecode import Bytecode

from wlvlang.vmobjects.boolean import Boolean
from wlvlang.vmobjects.integer import Integer


class DummyCompilationUnit(ast.Node):
    def __init__(self, code_to_emit):
        self.code_to_emit = chr(code_to_emit)

    def compile(self, context):
        context.emit(self.code_to_emit)

    def __repr__(self):
        return "DummyCompilationUnit(%r)" % self.code_to_emit

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

def test_ast_or_compiler():
    ctx = create_interpreter_context()
    node = ast.Or(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.compile(ctx)

    # Expect bytecode: [91, 90, Bytecode.OR]
    assert ctx.bytecode == [chr(91), chr(90), Bytecode.OR]

def test_ast_and_compiler():
    ctx = create_interpreter_context()
    node = ast.And(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.compile(ctx)

    assert ctx.bytecode == [chr(91), chr(90), Bytecode.AND]

def test_ast_equals_compiler():
    ctx = create_interpreter_context()
    node = ast.Equals(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.compile(ctx)

    assert ctx.bytecode == [chr(91), chr(90), Bytecode.EQUAL]
