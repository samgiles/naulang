from wlvlang.compiler.ssa import TACGen
from wlvlang.compiler import ast
from wlvlang.interpreter.space import ObjectSpace

def create_tac_generator():
    return TACGen(ObjectSpace())

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
    tacs = tac.get_tacs()
    assert tac.get_tacs() == {
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
