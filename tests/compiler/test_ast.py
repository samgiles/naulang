from wlvlang.compiler import ast

def test_ast_constant_integer():
    assert ast.ConstantInteger(10) == ast.ConstantInteger(10)
    assert ast.ConstantInteger(1231) != ast.ConstantInteger(123231)

def test_ast_constant_float():
    assert ast.ConstantFloat(1.0) == ast.ConstantFloat(1.0)
    assert ast.ConstantFloat(1.1) != ast.ConstantFloat(1.0)

def test_ast_send():
    assert ast.Send(ast.ConstantFloat(1.0), "+", [ast.ConstantFloat(1.0)]) == ast.Send(ast.ConstantFloat(1.0), "+", [ast.ConstantFloat(1.0)])
    assert ast.Send(ast.ConstantInteger(1), "+", [ast.ConstantFloat(1.0)]) != ast.Send(ast.ConstantFloat(1.0), "+", [ast.ConstantFloat(1.0)])

    # Test recursive equals
    assert ast.Send(
            ast.Send(ast.ConstantInteger(1), "*", [ast.ConstantInteger(1)]),
            "*",
            [ast.ConstantInteger(10)]) == ast.Send(ast.Send(ast.ConstantInteger(1), "*", [ast.ConstantInteger(1)]),"*", [ast.ConstantInteger(10)])

    assert ast.Send(
            ast.Send(ast.ConstantInteger(1), "*", [ast.ConstantInteger(1)]),
            "/",
            [ast.ConstantInteger(10)]) != ast.Send(ast.Send(ast.ConstantInteger(1), "*", [ast.ConstantInteger(1)]),"*", [ast.ConstantInteger(10)])
