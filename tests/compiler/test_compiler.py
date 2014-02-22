from wlvlang.compiler import ast
from wlvlang.compiler.context import MethodCompilerContext
from wlvlang.compiler.compiler import SyntaxDirectedTranslator

from wlvlang.vm.vm_universe import VM_Universe
from wlvlang.interpreter.bytecode import Bytecode

from wlvlang.vmobjects.boolean import Boolean
from wlvlang.vmobjects.integer import Integer


class DummyCompilationUnit(ast.Node):
    def __init__(self, code_to_emit):
        self.code_to_emit = chr(code_to_emit)

    def compile(self, context):
        context.emit(self.code_to_emit)

    def accept(self, visitor):
        visitor.visit_dummy(self)

    def __repr__(self):
        return "DummyCompilationUnit(%r)" % self.code_to_emit

def create_interpreter_context():
    universe = VM_Universe()
    ctx = MethodCompilerContext(universe)
    return ctx

def create_syntax_directed_translator(ctx):
    def dummy_visit(self, node):
        self._context.emit(node.code_to_emit)
        return True

    SyntaxDirectedTranslator.visit_dummy = dummy_visit
    return SyntaxDirectedTranslator(ctx)

def test_ast_integer_compile():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.IntegerConstant(100)
    node.accept(t)

    # Expect the constant to be stored in the literals area at position 0 (as this was a new context)
    assert ctx._literals[0] == Integer(100)

    # Expect the byte code to be [Bytecode.LOAD_CONST, 0]
    assert ctx.get_bytecode() == [Bytecode.LOAD_CONST, chr(0)]

def test_ast_boolean_constant_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.BooleanConstant(True)
    node.accept(t)

    # Expect the constant to be stored in the literals area at position 0 (as this was a new context)
    assert ctx._literals[0] == Boolean(True)

    # Expect the byte code to be [Bytecode.LOAD_CONST, 0]
    assert ctx.get_bytecode() == [Bytecode.LOAD_CONST, chr(0)]

def test_ast_assignment_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.ScopedAssignment('a', ast.BooleanConstant(True))
    node.accept(t)

    # Expect the constant to be stored in the literals area at position 0
    assert ctx._literals[0] == Boolean(True)

    # Expect the bytecode to be [Bytecode.LOAD_CONST, 0, Bytecode.STORE, 0]
    assert ctx.get_bytecode() == [Bytecode.LOAD_CONST, chr(0), Bytecode.STORE, chr(0)]

def test_ast_or_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.Or(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    # Expect bytecode: [91, 90, Bytecode.OR]
    assert ctx.get_bytecode() == [chr(91), chr(90), Bytecode.OR]

def test_ast_and_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.And(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(91), chr(90), Bytecode.AND]

def test_ast_equals_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.Equals(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(91), chr(90), Bytecode.EQUAL]

def test_ast_not_equals_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.NotEquals(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(91), chr(90), Bytecode.NOT_EQUAL]

def test_ast_lessthan_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.LessThan(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(91), chr(90), Bytecode.LESS_THAN]

def test_ast_lessthanorequal_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.LessThanOrEqual(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(91), chr(90), Bytecode.LESS_THAN_EQ]

def test_ast_greaterthanorequal_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.GreaterThanOrEqual(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(91), chr(90), Bytecode.GREATER_THAN_EQ]

def test_ast_greaterthan_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.GreaterThan(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(91), chr(90), Bytecode.GREATER_THAN]

def test_ast_addop_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.AddOp(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(91), chr(90), Bytecode.ADD]

def test_ast_subtractop_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.SubtractOp(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(91), chr(90), Bytecode.SUB]

def test_ast_mulop_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.MulOp(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(91), chr(90), Bytecode.MUL]

def test_ast_divop_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.DivOp(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(91), chr(90), Bytecode.DIV]

def test_ast_unarynot_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.UnaryNot(DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(90), Bytecode.NOT]

def test_ast_unarynegate_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.UnaryNegate(DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(90), Bytecode.NEG]

def test_ast_whilestatement_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    # Add padding to bytecodes to test non-zero based context (this is more realistic)
    ctx.emit(chr(100))
    node = ast.WhileStatement(DummyCompilationUnit(90), ast.Block([DummyCompilationUnit(91)]))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(100), chr(90), Bytecode.JUMP_IF_FALSE, chr(7), chr(91), Bytecode.JUMP_BACK, chr(1)]

def test_ast_ifstatement_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    # Add padding to bytecodes to test non-zero based context (this is more realistic)
    ctx.emit(chr(100))
    node = ast.IfStatement(DummyCompilationUnit(90), ast.Block([DummyCompilationUnit(91)]))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(100), chr(90), Bytecode.JUMP_IF_FALSE, chr(5), chr(91)]

def test_ast_printstatement():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.PrintStatement(DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(90), Bytecode.PRINT]

def test_ast_functionstatement():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.FunctionStatement('a', ast.ParameterList(['a']), ast.Block([DummyCompilationUnit(90)]))
    node.accept(t)

    assert ctx.get_bytecode() == [Bytecode.LOAD_CONST, chr(0)]
    assert len(ctx._inner_contexts) == 1
    assert ctx._inner_contexts[0].get_bytecode() == [chr(90), Bytecode.HALT]
    assert ctx._inner_contexts[0].has_local('a') == True
    assert ctx._inner_contexts[0].get_parameter_count() == 1

def test_ast_functionexpression():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.FunctionExpression(ast.ParameterList(['a']), ast.Block([DummyCompilationUnit(90)]))
    node.accept(t)

    assert ctx.get_bytecode() == [Bytecode.LOAD_CONST, chr(0)]
    assert len(ctx._inner_contexts) == 1
    assert ctx._inner_contexts[0].get_bytecode() == [chr(90), Bytecode.HALT]
    assert ctx._inner_contexts[0].has_local('a') == True
    assert ctx._inner_contexts[0].get_parameter_count() == 1

def test_ast_functioncall():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.FunctionCall('a', ast.FunctionArgList([DummyCompilationUnit(90), DummyCompilationUnit(91)]))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(90), chr(91), Bytecode.INVOKE, chr(0)]

def test_ast_returnstatement():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.ReturnStatement(DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(90), Bytecode.RETURN]

def test_array_access():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.ArrayAccess(DummyCompilationUnit(90), DummyCompilationUnit(91))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(90), chr(91), Bytecode.ARRAY_LOAD]

def test_array_access_assignment():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.ArrayAssignment(ast.ArrayAccess(DummyCompilationUnit(90), DummyCompilationUnit(91)), DummyCompilationUnit(93))
    node.accept(t)

    assert ctx.get_bytecode() == [chr(90), chr(91), chr(93), Bytecode.ARRAY_STORE]

def test_invoke_global_list():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.FunctionCall('list', ast.FunctionArgList([ast.IntegerConstant(10)]))
    node.accept(t)

    assert ctx.get_bytecode() == [Bytecode.LOAD_CONST, chr(0), Bytecode.INVOKE_GLOBAL, chr(0)]

def test_break_statement():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.WhileStatement(DummyCompilationUnit(90), ast.Block([ast.BreakStatement()]))
    node.accept(t)

    assert ctx.get_bytecode() == [
            chr(90),
            Bytecode.JUMP_IF_FALSE, chr(7),
            Bytecode.JUMP_BACK, chr(7),
            Bytecode.JUMP_BACK, chr(0)
        ]

def test_continue_statement():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.WhileStatement(DummyCompilationUnit(90), ast.Block([ast.ContinueStatement()]))
    node.accept(t)

    assert ctx.get_bytecode() == [
            chr(90),
            Bytecode.JUMP_IF_FALSE, chr(7),
            Bytecode.JUMP_BACK, chr(0),
            Bytecode.JUMP_BACK, chr(0)
        ]

def test_ast_scoped_assignment():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.Block([
                ast.ScopedAssignment('x', ast.IntegerConstant(10)),
                    ast.FunctionExpression(
                        ast.ParameterList(['a']),
                        ast.Block([
                            ast.Assignment('x', ast.IntegerConstant(12)),
                            ast.PrintStatement(ast.IdentifierExpression('x'))
                        ])
                    )
                ])

    """ AST Equivalent to:
            let x = 10
            fn(a) {
               x = 12
               print x
            }
    """

    node.accept(t)
    assert ctx._literals[0] == Integer(10)

    # Outer context loads the function expression constant from literals area 0
    assert ctx.get_bytecode() == [
            Bytecode.LOAD_CONST, chr(0),  # Push the constant at 0 onto the stack (10)
            Bytecode.STORE, chr(0),       # Store the top of the stack into locals aread at 0
            Bytecode.LOAD_CONST, chr(1)   # Push the function expression onto the top of the stack
        ]

    # Expect the constant to be stored in the literals area at position 0
    # Of the first inner method context
    inner_contexts = ctx.get_inner_contexts()
    assert len(inner_contexts) == 1
    assert inner_contexts[0]._literals[0] == Integer(12)

    assert inner_contexts[0].get_bytecode() == [
            Bytecode.LOAD_CONST, chr(0),            # Push 12 onto the stack
            Bytecode.STORE_DYNAMIC, chr(0), chr(1), # Store 12 into the dynamic variable x
            Bytecode.LOAD_DYNAMIC, chr(0), chr(1),  # Load dynamic variable x onto the top of the stack
            Bytecode.PRINT,                         # Call print
            Bytecode.HALT                           # All functions end in HALT
        ]

def test_ast_scoped_usage():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.Block([
            ast.ScopedAssignment('n', ast.IntegerConstant(10)),
            ast.ScopedAssignment('a', ast.FunctionExpression(
                ast.ParameterList(['x']),
                ast.Block([
                    ast.PrintStatement(
                        ast.AddOp(
                            ast.MulOp(
                                ast.IdentifierExpression('x'),
                                ast.IntegerConstant(2)
                            ),
                            ast.IdentifierExpression('n')
                        )
                    )
                ])
            )),
            ast.FunctionCall(
                'a',
                ast.FunctionArgList([ast.IntegerConstant(2)])
            ),
            ast.FunctionCall(
                'a',
                ast.FunctionArgList([ast.IntegerConstant(4)])
            )
        ])

    node.accept(t)

    assert ctx.get_bytecode() == [
            Bytecode.LOAD_CONST, chr(0),
            Bytecode.STORE, chr(0),
            Bytecode.LOAD_CONST, chr(1),
            Bytecode.STORE, chr(1),
            Bytecode.LOAD_CONST, chr(2),
            Bytecode.INVOKE, chr(1),
            Bytecode.LOAD_CONST, chr(3),
            Bytecode.INVOKE, chr(1),
    ]

    inner_contexts = ctx.get_inner_contexts()

    assert inner_contexts[0].get_bytecode() == [
        Bytecode.LOAD, chr(0),
        Bytecode.LOAD_CONST, chr(0),
        Bytecode.MUL,
        Bytecode.LOAD_DYNAMIC, chr(0), chr(1),
        Bytecode.ADD,
        Bytecode.PRINT,
        Bytecode.HALT
    ]
