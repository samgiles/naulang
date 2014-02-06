import pytest

from wlvlang.compiler.sourceparser import parse
from wlvlang.compiler import ast

def test_parse_constant_integer():
    assert parse("100") == ast.Block([ast.IntegerConstant(100)])
    assert parse("-100") == ast.Block([ast.IntegerConstant(-100)])

@pytest.mark.xfail
def test_parse_constant_float():
    p = Parser()

    assert p.parse("100.0") == ast.Main(ast.Block(ast.ConstantFloat(100.0)))
    assert p.parse("-100.0") == ast.Main(ast.Block(ast.ConstantFloat(-100.0)))
    assert p.parse("1.0E2") == ast.Main(ast.Block(ast.ConstantFloat(100.0)))
    assert p.parse("1.0e2") == ast.Main(ast.Block(ast.ConstantFloat(100.0)))

@pytest.mark.xfail
def test_binary_expression():
    p = Parser()

    assert p.parse("100+100") == ast.Main(ast.Block(ast.Expression(ast.Send(ast.ConstantInteger(100), "+", [ast.ConstantInteger(100)]))))
    assert p.parse("100-100") == ast.Main(ast.Block(ast.Expression(ast.Send(ast.ConstantInteger(100), "-", [ast.ConstantInteger(100)]))))
    assert p.parse("100/100") == ast.Main(ast.Block(ast.Expression(ast.Send(ast.ConstantInteger(100), "/", [ast.ConstantInteger(100)]))))
    assert p.parse("100%100") == ast.Main(ast.Block(ast.Expression(ast.Send(ast.ConstantInteger(100), "%", [ast.ConstantInteger(100)]))))
    assert p.parse("100*100") == ast.Main(ast.Block(ast.Expression(ast.Send(ast.ConstantInteger(100), "*", [ast.ConstantInteger(100)]))))
    assert p.parse("100 == 100") == ast.Main(ast.Block(ast.Expression(ast.Send(ast.ConstantInteger(100), "==", [ast.ConstantInteger(100)]))))
    assert p.parse("100 != 100") == ast.Main(ast.Block(ast.Expression(ast.Send(ast.ConstantInteger(100), "!=", [ast.ConstantInteger(100)]))))
    assert p.parse("100 and 100") == ast.Main(ast.Block(ast.Expression(ast.Send(ast.ConstantInteger(100), "and", [ast.ConstantInteger(100)]))))
    assert p.parse("100 or 100") == ast.Main(ast.Block(ast.Expression(ast.Send(ast.ConstantInteger(100), "or", [ast.ConstantInteger(100)]))))
    assert p.parse("100 < 100") == ast.Main(ast.Block(ast.Expression(ast.Send(ast.ConstantInteger(100), "<", [ast.ConstantInteger(100)]))))
    assert p.parse("100 > 100") == ast.Main(ast.Block(ast.Expression(ast.Send(ast.ConstantInteger(100), ">", [ast.ConstantInteger(100)]))))
    assert p.parse("100 >= 100") == ast.Main(ast.Block(ast.Expression(ast.Send(ast.ConstantInteger(100), ">=", [ast.ConstantInteger(100)]))))
    assert p.parse("100 <= 100") == ast.Main(ast.Block(ast.Expression(ast.Send(ast.ConstantInteger(100), "<=", [ast.ConstantInteger(100)]))))

