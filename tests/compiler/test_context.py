from naulang.compiler.context import FunctionCompilerContext
from naulang.interpreter.bytecode import Bytecode
from naulang.interpreter.objectspace.integer import Integer
def test_calculate_stack_depth():
    ctx = FunctionCompilerContext(None)
    code = [
            Bytecode.LOAD, 0,         # 1
            Bytecode.LOAD_CONST, 1,   # 1
            Bytecode.ADD,             # -1
            Bytecode.LOAD, 1,         # 1
            Bytecode.ADD,             # -1
            Bytecode.STORE, 1,        # -1
            Bytecode.LOAD, 1,         # 1
            Bytecode.LOAD, 2,         # 1
            Bytecode.LOAD, 3          # 1
        ]

    stack_depth = ctx._calculate_stack_depth(code)

    assert stack_depth == 3

def test_calculate_stack_depth2():
    ctx = FunctionCompilerContext(None)
    code = [Bytecode.LOAD_CONST, 0,         # 1
            Bytecode.JUMP_IF_FALSE, 37,     # -1
            Bytecode.LOAD, 0,               # 1
            Bytecode.CHAN_OUT,              # 0
            Bytecode.STORE, 2,              # -1
            Bytecode.LOAD, 2,               # 1
            Bytecode.LOAD_CONST, 1,         # 1
            Bytecode.GREATER_THAN,          # -1
            Bytecode.JUMP_IF_FALSE, 27,     # -1
            Bytecode.LOAD, 1,               # 1
            Bytecode.LOAD_CONST, 2,         # 1
            Bytecode.LOAD, 2,               # 1
            Bytecode.CHAN_OUT,              # 0
            Bytecode.ADD,                   # -1
            Bytecode.CHAN_IN,               # -2
            Bytecode.JUMP, 0,               # 0
            Bytecode.LOAD, 1,               # 1
            Bytecode.LOAD, 2,               # 1
            Bytecode.CHAN_OUT,              # 0
            Bytecode.CHAN_IN,               # -2
            Bytecode.JUMP, 37,              # 0
            Bytecode.JUMP, 0,               # 0
            Bytecode.HALT]                  # 0

    stack_depth = ctx._calculate_stack_depth(code)
    assert stack_depth == 3

def test_register_literal_unique_only():
    ctx = FunctionCompilerContext(None)
    inta = Integer(10)
    intb = Integer(10)
    intc = Integer(100)

    inta_num = ctx.register_literal(inta)
    intc_num = ctx.register_literal(intc)
    intb_num = ctx.register_literal(intb)

    # First literal to be registered so should be 0
    assert 0 == inta_num

    # inta_num and intb_num should be identical as the literal
    # bojects that were registered are equivalent.
    assert inta_num == intb_num

    # intb_num whould be the next literal slot 1
    assert 1 == intc_num


def test_register_local():
    ctx = FunctionCompilerContext(None)

    x = ctx.register_local('x')
    y = ctx.register_local('y')

    assert x == 0
    assert y == 1
    assert x == ctx.register_local('x')


def test_register_dynamic():
    """ If a local has been registered in an outer context,
    it should be accessible from an inner context via register_dynamic """
    outer = FunctionCompilerContext(None)
    outer_idx = outer.register_local('x')

    inner = FunctionCompilerContext(None, outer=outer)

    index, level = inner.register_dynamic('x')

    assert index == outer_idx
    assert level == 1
