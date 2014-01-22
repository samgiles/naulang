from wlvlang.compiler import ast

def test_ast_constant_integer():
    assert ast.ConstantInteger(10) == ast.ConstantInteger(10)
    assert ast.ConstantInteger(1231) != ast.ConstantInteger(123231)

def test_ast_constant_float():
    assert ast.ConstantFloat(1.0) == ast.ConstantFloat(1.0)
    assert ast.ConstantFloat(1.1) != ast.ConstantFloat(1.0)
