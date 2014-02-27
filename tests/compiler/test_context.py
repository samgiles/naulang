from wlvlang.compiler.context import FunctionCompilerContext
from wlvlang.interpreter.bytecode import Bytecode
def test_calculate_stack_depth():
    ctx = FunctionCompilerContext(None)
    code = [
            Bytecode.LOAD, 0,
            Bytecode.LOAD_CONST, 1,
            Bytecode.ADD,
            Bytecode.LOAD, 1,
            Bytecode.ADD,
            Bytecode.STORE, 1,
            Bytecode.LOAD, 1,
            Bytecode.LOAD, 2,
            Bytecode.LOAD, 3
        ]

    stack_depth = ctx._calculate_stack_depth(code)

    assert stack_depth == 5
