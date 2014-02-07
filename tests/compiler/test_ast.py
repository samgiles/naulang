from wlvlang.compiler import ast
from wlvlang.compiler.context import MethodCompilerContext

from wlvlang.vm.vm_universe import VM_Universe
from wlvlang.interpreter.bytecode import Bytecode

from wlvlang.vmobjects.boolean import Boolean
from wlvlang.vmobjects.integer import Integer

class DummyNode(ast.Node):

    def __init__(self, value):
        self.value = value

    def compile(self, context):
        pass

    def __repr__(self):
        return "DummyNode(%r)" % self.value



def test_ast_integer_constant():
    assert ast.IntegerConstant(10) == ast.IntegerConstant(10)
    assert ast.IntegerConstant(1231) != ast.IntegerConstant(123231)


def test_ast_boolean_constant():
    assert ast.BooleanConstant(True) == ast.BooleanConstant(True)
    assert ast.BooleanConstant(False) == ast.BooleanConstant(False)

def test_ast_assignment():
    assert ast.Assignment('a', DummyNode(100)) == ast.Assignment('a', DummyNode(100))
    assert ast.Assignment('a', DummyNode(10)) != ast.Assignment('a', DummyNode(100))


def test_ast_statement():
    assert ast.Statement(DummyNode(True)) == ast.Statement(DummyNode(True))
    assert ast.Statement(DummyNode(False)) != ast.Statement(DummyNode(True))


