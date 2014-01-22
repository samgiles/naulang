from wlvlang.compiler import ast

def test_ast_constant_integer():
    assert ast.ConstantInteger(10) == ast.ConstantInteger(10)
    assert ast.ConstantInteger(1231) != ast.ConstantInteger(123231)
