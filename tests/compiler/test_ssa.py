from wlvlang.compiler.ssa import TACGen
from wlvlang.compiler import ast
from wlvlang.interpreter.space import ObjectSpace

def create_tac_generator():
    return SSAGen(ObjectSpace())

def test_print_statement():
    tac = create_tac_generator()
    node = ast.WhileStatement(ast.BooleanConstant(True), ast.Block([ast.BooleanConstant(True)]))
    node.accept(tac)

    root_block = tac.get_root_block()
    root_block.get_tacs() == { "v0": (ast.Operator.CONST, True, None), "v1": (ast.Operator.PRINT, "v0", None) }

def test_while_statement():
    '''     Tests that we end up with a graph like:

                R---C[true|false]
                       |     |--------------B
                       |                   /
                       |------------------A

            for code:
                while True {
                    dostuff
                }
    '''
    tac = create_tac_generator()
    node = ast.WhileStatement(ast.BooleanConstant(True), ast.Block([ast.BooleanConstant(True)]))
    node.accept(tac)

    root_block = tac.get_root_block()
    assert root_block.next_block.get_tacs() == { "v0": (ast.Operator.CONST, True, None) }
    assert root_block.next_block.true_block.get_tacs() == { "v1": (ast.Operator.CONST, True, None) }
    assert root_block.next_block.false_block.get_tacs() == {}
    assert root_block.next_block.previous_blocks[0] is root_block

def test_continue_statement():
    '''     Tests that we end up with a graph like:

                R---C[true|false]
                       | ^    |--------------B
                       |  \
                       |---A

            for code:
                while True {
                    continue
                }
    '''
    tac = create_tac_generator()
    node = ast.WhileStatement(ast.BooleanConstant(True), ast.Block([ast.BooleanConstant(True), ast.ContinueStatement()]))
    node.accept(tac)

    root_block = tac.get_root_block()
    assert root_block.next_block.true_block.next_block.next_block is root_block.next_block

def test_break_statement():
    """     Tests that we end up with a graph like:

                R---C[true|false]
                       |     |--------------B
                       |                   /
                       |-----------------A/

            for code:
                while True {
                    break
                }
    """
    tac = create_tac_generator()
    node = ast.WhileStatement(ast.BooleanConstant(True), ast.Block([ast.BooleanConstant(True), ast.BreakStatement()]))
    node.accept(tac)

    root_block = tac.get_root_block()
    assert root_block.next_block.true_block.get_tacs() == { "v1": (ast.Operator.CONST, True, None) }
    assert root_block.next_block.true_block.next_block.next_block is root_block.next_block.false_block

def test_if_statement():
    tac = create_tac_generator()
    node = ast.IfStatement(ast.BooleanConstant(True), ast.Block([ast.BooleanConstant(True)]))
    node.accept(tac)

    root_block = tac.get_root_block()
    assert root_block.next_block.get_tacs() == { "v0": (ast.Operator.CONST, True, None) }
    assert root_block.next_block.true_block.get_tacs() == { "v1": (ast.Operator.CONST, True, None) }
    assert root_block.next_block.false_block.get_tacs() == {}
    assert root_block.next_block.false_block.previous_blocks == [root_block.next_block, root_block.next_block.true_block]


def test_addition_expression():
    tac = create_tac_generator()
    node = ast.Add(
        ast.Add(
            ast.Subtract(
                ast.Multiply(
                    ast.IntegerConstant(10),
                    ast.IntegerConstant(6)
                ),
                ast.IntegerConstant(5)
            ),
            ast.IntegerConstant(2)
        ),
        ast.Divide(
            ast.IntegerConstant(1000),
            ast.IntegerConstant(2)
        )
    )

    node.accept(tac)
    tacs = tac.get_current_block().get_tacs()
    assert tacs == {
        "v0": (ast.Operator.CONST, 10, None),
        "v1": (ast.Operator.CONST, 6, None),
        "v2": (ast.Operator.MUL, "v0", "v1"),
        "v3": (ast.Operator.CONST, 5, None),
        "v4": (ast.Operator.SUB, "v2", "v3"),
        "v5": (ast.Operator.CONST, 2, None),
        "v6": (ast.Operator.ADD, "v4", "v5"),
        "v7": (ast.Operator.CONST, 1000, None),
        "v8": (ast.Operator.CONST, 2, None),
        "v9": (ast.Operator.DIV, "v7", "v8"),
        "v10": (ast.Operator.ADD, "v6", "v9")
    }
