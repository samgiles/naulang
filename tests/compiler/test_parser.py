import pytest

@pytest.mark.xfail
def test_parse_constant_integer():
    p = Parser()

    assert p.parse("100") == ast.Main(ast.Block(ast.ConstantInteger(100)))
    assert p.parse("-100") == ast.Main(ast.Block(ast.ConstantInteger(-100)))
    assert p.parse("0x64") == ast.Main(ast.Block(ast.ConstantInteger(100)))
    assert p.parse("0o144") == ast.Main(ast.Block(ast.ConstantInteger(100)))
    assert p.parse("0b1100100") == ast.Main(ast.Block(ast.ConstantInteger(100)))

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

