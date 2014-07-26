from naulang.compiler import ast


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


def test_ast_float_constant():
    assert ast.FloatConstant(10.1) == ast.FloatConstant(10.1)
    assert ast.FloatConstant(10.2) != ast.FloatConstant(10.1)


def test_ast_boolean_constant():
    assert ast.BooleanConstant(True) == ast.BooleanConstant(True)
    assert ast.BooleanConstant(False) == ast.BooleanConstant(False)


def test_ast_assignment():
    assert ast.Assignment('a', DummyNode(100)) == ast.Assignment('a', DummyNode(100))
    assert ast.Assignment('a', DummyNode(10)) != ast.Assignment('a', DummyNode(100))


def test_ast_or():
    assert ast.Or(DummyNode(True), DummyNode(True)) == ast.Or(DummyNode(True), DummyNode(True))
    assert ast.Or(DummyNode(False), DummyNode(True)) != ast.Or(DummyNode(True), DummyNode(True))


def test_ast_and():
    assert ast.And(DummyNode(True), DummyNode(True)) == ast.And(DummyNode(True), DummyNode(True))
    assert ast.And(DummyNode(False), DummyNode(True)) != ast.And(DummyNode(True), DummyNode(True))


def test_ast_equals():
    assert ast.Equals(DummyNode(True), DummyNode(True)) == ast.Equals(DummyNode(True), DummyNode(True))
    assert ast.Equals(DummyNode(False), DummyNode(True)) != ast.Equals(DummyNode(True), DummyNode(True))


def test_ast_notequals():
    assert ast.NotEquals(DummyNode(True), DummyNode(True)) == ast.NotEquals(DummyNode(True), DummyNode(True))
    assert ast.NotEquals(DummyNode(False), DummyNode(True)) != ast.NotEquals(DummyNode(True), DummyNode(True))


def test_ast_lessthan():
    assert ast.LessThan(DummyNode(True), DummyNode(True)) == ast.LessThan(DummyNode(True), DummyNode(True))
    assert ast.LessThan(DummyNode(False), DummyNode(True)) != ast.LessThan(DummyNode(True), DummyNode(True))


def test_ast_lessthanorequal():
    assert ast.LessThanOrEqual(
        DummyNode(True),
        DummyNode(True)) == ast.LessThanOrEqual(DummyNode(True), DummyNode(True))
    assert ast.LessThanOrEqual(
        DummyNode(False),
        DummyNode(True)) != ast.LessThanOrEqual(DummyNode(True), DummyNode(True))


def test_ast_greaterthanorequal():
    assert ast.GreaterThanOrEqual(
        DummyNode(True),
        DummyNode(True)) == ast.GreaterThanOrEqual(DummyNode(True), DummyNode(True))
    assert ast.GreaterThanOrEqual(
        DummyNode(False),
        DummyNode(True)) != ast.GreaterThanOrEqual(DummyNode(True), DummyNode(True))


def test_ast_greaterthan():
    assert ast.GreaterThan(DummyNode(True), DummyNode(True)) == ast.GreaterThan(DummyNode(True), DummyNode(True))
    assert ast.GreaterThan(DummyNode(False), DummyNode(True)) != ast.GreaterThan(DummyNode(True), DummyNode(True))


def test_ast_addop():
    assert ast.Add(DummyNode(True), DummyNode(True)) == ast.Add(DummyNode(True), DummyNode(True))
    assert ast.Add(DummyNode(False), DummyNode(True)) != ast.Add(DummyNode(True), DummyNode(True))


def test_ast_subtractop():
    assert ast.Subtract(DummyNode(True), DummyNode(True)) == ast.Subtract(DummyNode(True), DummyNode(True))
    assert ast.Subtract(DummyNode(False), DummyNode(True)) != ast.Subtract(DummyNode(True), DummyNode(True))


def test_ast_mulop():
    assert ast.Multiply(DummyNode(True), DummyNode(True)) == ast.Multiply(DummyNode(True), DummyNode(True))
    assert ast.Multiply(DummyNode(False), DummyNode(True)) != ast.Multiply(DummyNode(True), DummyNode(True))


def test_ast_divop():
    assert ast.Divide(DummyNode(True), DummyNode(True)) == ast.Divide(DummyNode(True), DummyNode(True))
    assert ast.Divide(DummyNode(False), DummyNode(True)) != ast.Divide(DummyNode(True), DummyNode(True))


def test_ast_unarynot():
    assert ast.UnaryNot(DummyNode(True)) == ast.UnaryNot(DummyNode(True))
    assert ast.UnaryNot(DummyNode(False)) != ast.UnaryNot(DummyNode(True))


def test_ast_unarynegate():
    assert ast.UnaryNegate(DummyNode(True)) == ast.UnaryNegate(DummyNode(True))
    assert ast.UnaryNegate(DummyNode(False)) != ast.UnaryNegate(DummyNode(True))


def test_ast_whilestatement():
    assert ast.WhileStatement(DummyNode(True),
                              ast.Block([DummyNode(True)])) == ast.WhileStatement(DummyNode(True),
                                                                                  ast.Block([DummyNode(True)]))
    assert ast.WhileStatement(DummyNode(False),
                              ast.Block([DummyNode(True)])) != ast.WhileStatement(DummyNode(True),
                                                                                  ast.Block([DummyNode(True)]))


def test_ast_ifstatement():
    assert ast.IfStatement(DummyNode(True),
                           ast.Block([DummyNode(True)])) == ast.IfStatement(DummyNode(True),
                                                                            ast.Block([DummyNode(True)]))
    assert ast.IfStatement(DummyNode(False),
                           ast.Block([DummyNode(True)])) != ast.IfStatement(DummyNode(True),
                                                                            ast.Block([DummyNode(True)]))


def test_ast_printstatement():
    assert ast.PrintStatement(DummyNode(10)) == ast.PrintStatement(DummyNode(10))
    assert ast.PrintStatement(DummyNode(11)) != ast.PrintStatement(DummyNode(10))


def test_ast_functionstatement():
    assert ast.FunctionStatement('a',
                                 ['a'],
                                 ast.Block([DummyNode(10)])) == ast.FunctionStatement('a',
                                                                                      ['a'],
                                                                                      ast.Block([DummyNode(10)]))
    assert ast.FunctionStatement('a',
                                 ['b'],
                                 ast.Block([DummyNode(10)])) != ast.FunctionStatement('a',
                                                                                      ['a'],
                                                                                      ast.Block([DummyNode(10)]))


def test_ast_scopedassignment():
    assert ast.ScopedAssignment('a', DummyNode(10)) == ast.ScopedAssignment('a', DummyNode(10))
    assert ast.ScopedAssignment('b', DummyNode(10)) != ast.ScopedAssignment('a', DummyNode(10))
