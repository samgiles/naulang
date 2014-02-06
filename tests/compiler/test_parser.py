import pytest

from wlvlang.compiler.sourceparser import parse
from wlvlang.compiler import ast

def test_parse_constant_integer():
    assert parse("0") == ast.Block([ast.IntegerConstant(0)])
    assert parse("100") == ast.Block([ast.IntegerConstant(100)])
    assert parse("-100") == ast.Block([ast.UnaryNegate(ast.IntegerConstant(100))])

@pytest.mark.xfail
def test_parse_constant_float():
    p = Parser()

    assert p.parse("100.0") == ast.Main(ast.Block(ast.ConstantFloat(100.0)))
    assert p.parse("-100.0") == ast.Main(ast.Block(ast.ConstantFloat(-100.0)))
    assert p.parse("1.0E2") == ast.Main(ast.Block(ast.ConstantFloat(100.0)))
    assert p.parse("1.0e2") == ast.Main(ast.Block(ast.ConstantFloat(100.0)))

def test_binary_expression():
    assert parse("100+100") == ast.Block([ast.AddOp(ast.IntegerConstant(100), ast.IntegerConstant(100))])
    assert parse("100-100") == ast.Block([ast.SubtractOp(ast.IntegerConstant(100), ast.IntegerConstant(100))])
    assert parse("100/100") == ast.Block([ast.DivOp(ast.IntegerConstant(100), ast.IntegerConstant(100))])
    # TODO assert parse("100%100") == ast.Block([ast.ModOp(ast.IntegerConstant(100), ast.IntegerConstant(100))])
    assert parse("100*100") == ast.Block([ast.MulOp(ast.IntegerConstant(100), ast.IntegerConstant(100))])
    assert parse("100 == 100") == ast.Block([ast.Equals(ast.IntegerConstant(100), ast.IntegerConstant(100))])
    assert parse("100 != 100") == ast.Block([ast.NotEquals(ast.IntegerConstant(100), ast.IntegerConstant(100))])
    assert parse("100 and 100") == ast.Block([ast.And(ast.IntegerConstant(100), ast.IntegerConstant(100))])
    assert parse("100 or 100") == ast.Block([ast.Or(ast.IntegerConstant(100), ast.IntegerConstant(100))])
    assert parse("100 < 100") == ast.Block([ast.LessThan(ast.IntegerConstant(100), ast.IntegerConstant(100))])
    assert parse("100 > 100") == ast.Block([ast.GreaterThan(ast.IntegerConstant(100), ast.IntegerConstant(100))])
    assert parse("100 >= 100") == ast.Block([ast.GreaterThanOrEqual(ast.IntegerConstant(100), ast.IntegerConstant(100))])
    assert parse("100 <= 100") == ast.Block([ast.LessThanOrEqual(ast.IntegerConstant(100), ast.IntegerConstant(100))])

def test_if_statement():
    assert(parse("""if (true) {
        100
        200
    }""") == ast.Block([ast.IfStatement(ast.BooleanConstant(True), ast.Block([ast.IntegerConstant(100), ast.IntegerConstant(200)]))]))

def test_while_statement():
    assert(parse("""while (true) {
        100
        200
    }""") == ast.Block([ast.WhileStatement(ast.BooleanConstant(True), ast.Block([ast.IntegerConstant(100), ast.IntegerConstant(200)]))]))

def test_print_statement():
    assert(parse("print true") == ast.Block([ast.PrintStatement(ast.BooleanConstant(True))]))

def test_boolean_literal():
    assert(parse("true") == ast.Block([ast.BooleanConstant(True)]))
    assert(parse("false") == ast.Block([ast.BooleanConstant(False)]))

def test_function_statement():
    assert parse("""fn(a, b) {
            100
        }""") == ast.Block([ast.FunctionStatement(['a', 'b'], ast.Block([ast.IntegerConstant(100)]))])

    assert parse("""fn() {
        100
    }""") == ast.Block([ast.FunctionStatement([], ast.Block([ast.IntegerConstant(100)]))])

def test_function_call_statement():
    print repr(parse("a()"))
    assert parse("a()") == ast.Block([ast.FunctionCall('a', [])])
    print repr(parse("""a()
                        b(10, a, 0) """))
    assert parse("""a()
                    b(10, a, 0) """) == ast.Block([ast.FunctionCall('a', []), ast.FunctionCall('b', [ast.IntegerConstant(10), ast.IdentifierExpression('a'), ast.IntegerConstant(0)])])

def test_return_statement():
    assert parse("""fn() {
        return 10
    }""") == ast.Block([ast.FunctionStatement([], ast.Block([ast.ReturnStatement(ast.IntegerConstant(10))]))])
