from wlvlang.compiler.sourceparser import parse
from wlvlang.compiler.context import MethodCompilerContext
from wlvlang.vm.vm_universe import VM_Universe
from wlvlang.interpreter.interpreter import Interpreter
from wlvlang.interpreter.bytecode import Bytecode
from wlvlang.interpreter.activationrecord import ActivationRecord

def test_compile_function():
    universe = VM_Universe()
    interpreter = Interpreter(universe)

    root_context = MethodCompilerContext(universe)
    ast = parse("""a = 10 * 10
                print a""")

    ast.compile(root_context)
    root_context.bytecode.append(Bytecode.HALT)
    method = root_context.generate_method()
    arec = ActivationRecord(
        root_context._locals + root_context._literals,
        len(root_context._locals),
        len(root_context._literals),
        10,
        None,
        access_link=None)

    interpreter.interpret(method, arec)
    assert False

