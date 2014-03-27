from wlvlang.compiler.ssa import TACGen, Operator, GraphNode
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
    import pytest;pytest.set_trace()
    assert tac.get_tacs() == {
        "v0": (Operator.CONST, 10, None),
        "v1": (Operator.CONST, 6, None),
        "v2": (Operator.MUL, "v0", "v1"),
        "v3": (Operator.CONST, 5, None),
        "v4": (Operator.SUB, "v2", "v3"),
        "v5": (Operator.CONST, 2, None),
        "v6": (Operator.ADD, "v4", "v5"),
        "v7": (Operator.CONST, 1000, None),
        "v8": (Operator.CONST, 2, None),
        "v9": (Operator.DIV, "v7", "v8"),
        "v10": (Operator.ADD, "v6", "v9")
    }
