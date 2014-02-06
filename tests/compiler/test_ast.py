from wlvlang.compiler import ast

class DummyNode(ast.Node):

    def __init__(self, value):
        self.value = value

    def compile(self, context):
        pass

    def __repr__(self):
        return "DummyNode(%r)" % self.value

def test_ast_integer_constant():
    assert ast.IntegerConstant(10) == ast.ConstantInteger(10)
    assert ast.IntegerConstant(1231) != ast.IntegerConstant(123231)

def test_ast_statement():
    assert ast.Statement(DummyNode(True)) == ast.Statement(DummyNode(True))
    assert ast.Statement(DummyNode(False)) != ast.Statement(DummyNode(True))
