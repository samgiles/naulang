from wlvlang.compiler import ast

def test_ast_integer_constant():
    assert ast.IntegerConstant(10) == ast.ConstantInteger(10)
    assert ast.IntegerConstant(1231) != ast.IntegerConstant(123231)


