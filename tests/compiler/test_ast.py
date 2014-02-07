from wlvlang.compiler import ast
from wlvlang.compiler.context import MethodCompilerContext

from wlvlang.vm.vm_universe import VM_Universe
from wlvlang.interpreter.bytecode import Bytecode

from wlvlang.vmobjects.boolean import Boolean

class DummyNode(ast.Node):

    def __init__(self, value):
        self.value = value

    def compile(self, context):
        pass

    def __repr__(self):
        return "DummyNode(%r)" % self.value

def create_interpreter_context():
    universe = VM_Universe()
    ctx = MethodCompilerContext(universe)
    return ctx


def test_ast_integer_constant():
    assert ast.IntegerConstant(10) == ast.IntegerConstant(10)
    assert ast.IntegerConstant(1231) != ast.IntegerConstant(123231)

def test_ast_boolean_constant():
    assert ast.BooleanConstant(True) == ast.BooleanConstant(True)
    assert ast.BooleanConstant(False) == ast.BooleanConstant(False)

def test_ast_boolean_constant_compiler():
    ctx = create_interpreter_context()
    node = ast.BooleanConstant(True)
    node.compile(ctx)

    # Expect the constant to be stored in the literals area at position 0 (as this was a new context)
    assert ctx._literals[0] == Boolean(True)

    # Expect the byte code to be [Bytecode.LOAD_CONST, 0]
    assert ctx.bytecode == [Bytecode.LOAD_CONST, chr(0)]


def test_ast_statement():
    assert ast.Statement(DummyNode(True)) == ast.Statement(DummyNode(True))
    assert ast.Statement(DummyNode(False)) != ast.Statement(DummyNode(True))


