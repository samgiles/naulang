from wlvlang.compiler import ast
from wlvlang.compiler.optimiser import ConstantFolding

def test_constant_integer_addop_folding():
    cf_optimiser = ConstantFolding()
    tree = ast.AddOp(ast.IntegerConstant(100), ast.IntegerConstant(200))

    result = tree.accept(cf_optimiser)
    assert result == ast.IntegerConstant(300)

def test_constant_integer_subtractop_folding():
    cf_optimiser = ConstantFolding()
    tree = ast.SubtractOp(ast.IntegerConstant(500), ast.IntegerConstant(200))

    result = tree.accept(cf_optimiser)
    assert result == ast.IntegerConstant(300)
