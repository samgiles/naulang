import pytest

from wlvlang.compiler.sourceparser import parse
from wlvlang.compiler import ast

def test_parse_constant_integer():
    assert parse("0") == ast.Block([ast.IntegerConstant(0)])
    assert parse("100") == ast.Block([ast.IntegerConstant(100)])
    assert parse("-100") == ast.Block([ast.UnaryNegate(ast.IntegerConstant(100))])

def test_parse_constant_float():
    assert parse("100.0") == ast.Block([ast.FloatConstant(100.0)])
    assert parse("-100.0") == ast.Block([ast.UnaryNegate(ast.FloatConstant(100.0))])
    assert parse("1.0E2") == ast.Block([ast.FloatConstant(100.0)])
    assert parse("1.0e2") == ast.Block([ast.FloatConstant(100.0)])

def test_addition_expression():
    assert parse("100+100") == ast.Block([ast.AddOp(ast.IntegerConstant(100), ast.IntegerConstant(100))])

def test_subtraction_expression():
    assert parse("100-100") == ast.Block([ast.SubtractOp(ast.IntegerConstant(100), ast.IntegerConstant(100))])

def test_division_expression():
    assert parse("100/100") == ast.Block([ast.DivOp(ast.IntegerConstant(100), ast.IntegerConstant(100))])

def test_modulo_expression():
    assert parse("100%100") == ast.Block([ast.ModOp(ast.IntegerConstant(100), ast.IntegerConstant(100))])

def test_multiply_expression():
    assert parse("100*100") == ast.Block([ast.MulOp(ast.IntegerConstant(100), ast.IntegerConstant(100))])

def test_equality_expression():
    assert parse("100 == 100") == ast.Block([ast.Equals(ast.IntegerConstant(100), ast.IntegerConstant(100))])
    assert parse("100 is 100") == ast.Block([ast.Equals(ast.IntegerConstant(100), ast.IntegerConstant(100))])

def test_not_equal_expression():
    assert parse("100 != 100") == ast.Block([ast.NotEquals(ast.IntegerConstant(100), ast.IntegerConstant(100))])

def test_logical_and_expression():
    assert parse("100 and 100") == ast.Block([ast.And(ast.IntegerConstant(100), ast.IntegerConstant(100))])

def test_logical_or_expression():
    assert parse("100 or 100") == ast.Block([ast.Or(ast.IntegerConstant(100), ast.IntegerConstant(100))])

def test_less_than_expression():
    assert parse("100 < 100") == ast.Block([ast.LessThan(ast.IntegerConstant(100), ast.IntegerConstant(100))])

def test_greater_than_expression():
    assert parse("100 > 100") == ast.Block([ast.GreaterThan(ast.IntegerConstant(100), ast.IntegerConstant(100))])

def test_greater_than_eq_expression():
    assert parse("100 >= 100") == ast.Block([ast.GreaterThanOrEqual(ast.IntegerConstant(100), ast.IntegerConstant(100))])

def test_less_than_eq_expression():
    assert parse("100 <= 100") == ast.Block([ast.LessThanOrEqual(ast.IntegerConstant(100), ast.IntegerConstant(100))])


def test_compound_expression():
    assert parse("10 * 6 - 5 + 2 + 1000 / 2") == ast.Block([
    ast.AddOp(
        ast.AddOp(
            ast.SubtractOp(
                ast.MulOp(
                    ast.IntegerConstant(10),
                    ast.IntegerConstant(6)
                ),
                ast.IntegerConstant(5)
            ),
            ast.IntegerConstant(2)
        ),
        ast.DivOp(
            ast.IntegerConstant(1000),
            ast.IntegerConstant(2)
        )
    )])

def test_if_statement():
    assert parse("""if true {
        100
    }""") == ast.Block([ast.IfStatement(ast.BooleanConstant(True), ast.Block([ast.IntegerConstant(100)]))])

def test_while_statement():
    assert(parse("""while true {
        100
        200
    }""") == ast.Block([ast.WhileStatement(ast.BooleanConstant(True), ast.Block([ast.IntegerConstant(100), ast.IntegerConstant(200)]))]))

def test_print_statement():
    assert parse("print 10") == ast.Block([ast.PrintStatement(ast.IntegerConstant(10))])

def test_boolean_literal():
    assert(parse("true") == ast.Block([ast.BooleanConstant(True)]))
    assert(parse("false") == ast.Block([ast.BooleanConstant(False)]))

def test_function_expression():
    assert parse("""fn(a, b) {
            100
        }""") == ast.Block([ast.FunctionExpression(ast.ParameterList(['a', 'b']), ast.Block([ast.IntegerConstant(100)]))])

def test_function_expression_one_arg():
    assert parse("""fn(a) {
        100
    }""") == ast.Block([ast.FunctionExpression(ast.ParameterList(['a']), ast.Block([ast.IntegerConstant(100)]))])

def test_function_expression_no_args():
    assert parse("""fn() {
        100
    }""") == ast.Block([ast.FunctionExpression(ast.ParameterList([]), ast.Block([ast.IntegerConstant(100)]))])

def test_function_call_statement():
    assert parse("a()") == ast.Block([ast.FunctionCall('a', ast.FunctionArgList([]))])

def test_function_call_statement_arguments():
    assert parse("""b(10, a, 0) """) == ast.Block([ast.FunctionCall('b', ast.FunctionArgList([ast.IntegerConstant(10), ast.IdentifierExpression('a'), ast.IntegerConstant(0)]))])

def test_return_statement():
    assert parse("""return 10""") == ast.Block([ast.ReturnStatement(ast.IntegerConstant(10))])

def test_expression_assignment():
    assert parse("""a = 10 * 10""") == ast.Block([ast.Assignment('a', ast.MulOp(ast.IntegerConstant(10), ast.IntegerConstant(10)))])

def test_function_statement_noarg():
    assert parse("""fn a() {
        100
    }""") == ast.Block([ast.FunctionStatement('a', ast.ParameterList([]), ast.Block([ast.IntegerConstant(100)]))])

def test_function_statement_onearg():
    assert parse("""fn a(x) {
        100
    }""") == ast.Block([ast.FunctionStatement('a', ast.ParameterList(['x']), ast.Block([ast.IntegerConstant(100)]))])

def test_function_statement_args():
    assert parse("""fn a(x, y, z) {
        100
    }""") == ast.Block([ast.FunctionStatement('a', ast.ParameterList(['x', 'y', 'z']), ast.Block([ast.IntegerConstant(100)]))])

def test_array_access():
    assert parse("""a[10]""") == ast.Block([ast.ArrayAccess(ast.IdentifierExpression('a'), ast.IntegerConstant(10))])
