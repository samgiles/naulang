from wlvlang.compiler import ast
from wlvlang.compiler.context import FunctionCompilerContext
from wlvlang.compiler.compiler import SyntaxDirectedTranslator

from wlvlang.interpreter.space import ObjectSpace
from wlvlang.interpreter.bytecode import Bytecode

from wlvlang.interpreter.objectspace.integer import Integer
from wlvlang.interpreter.objectspace.boolean import Boolean

class DummyCompilationUnit(ast.Node):
    def __init__(self, code_to_emit):
        self.code_to_emit = code_to_emit

    def compile(self, context):
        context.emit(self.code_to_emit)

    def accept(self, visitor):
        visitor.visit_dummycompilationunit(self)

    def __repr__(self):
        return "DummyCompilationUnit(%r)" % self.code_to_emit

def create_interpreter_context():
    space = ObjectSpace()
    ctx = FunctionCompilerContext(space)
    return ctx

def create_syntax_directed_translator(ctx):
    def dummy_visit(self, node):
        self.context.emit(node.code_to_emit)
        return True

    # Patch the visit dummy method on to the translator
    SyntaxDirectedTranslator.visit_dummycompilationunit = dummy_visit
    return SyntaxDirectedTranslator(ctx)

def test_ast_integer_compile():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.IntegerConstant(100)
    node.accept(t)

    # Expect the constant to be stored in the literals area at position 0 (as this was a new context)
    assert ctx.literals[0] == Integer(100)

    # Expect the byte code to be [Bytecode.LOAD_CONST, 0]
    assert ctx.get_bytecode() == [Bytecode.LOAD_CONST, 0]

def test_ast_boolean_constant_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.BooleanConstant(True)
    node.accept(t)

    # Expect the constant to be stored in the literals area at position 0 (as this was a new context)
    assert ctx.literals[0] == Boolean(True)

    # Expect the byte code to be [Bytecode.LOAD_CONST, 0]
    assert ctx.get_bytecode() == [Bytecode.LOAD_CONST, 0]

def test_ast_assignment_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.ScopedAssignment('a', ast.BooleanConstant(True))
    node.accept(t)

    # Expect the constant to be stored in the literals area at position 0
    assert ctx.literals[0] == Boolean(True)

    # Expect the bytecode to be [Bytecode.LOAD_CONST, 0, Bytecode.STORE, 0]
    assert ctx.get_bytecode() == [Bytecode.LOAD_CONST, 0, Bytecode.STORE, 0]

def test_ast_or_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.Or(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    # Expect bytecode: [91, 90, Bytecode.OR]
    assert ctx.get_bytecode() == [91, 90, Bytecode.OR]

def test_ast_and_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.And(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [91, 90, Bytecode.AND]

def test_ast_equals_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.Equals(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [91, 90, Bytecode.EQUAL]

def test_ast_not_equals_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.NotEquals(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [91, 90, Bytecode.NOT_EQUAL]

def test_ast_lessthan_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.LessThan(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [91, 90, Bytecode.LESS_THAN]

def test_ast_lessthanorequal_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.LessThanOrEqual(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [91, 90, Bytecode.LESS_THAN_EQ]

def test_ast_greaterthanorequal_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.GreaterThanOrEqual(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [91, 90, Bytecode.GREATER_THAN_EQ]

def test_ast_greaterthan_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.GreaterThan(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [91, 90, Bytecode.GREATER_THAN]

def test_ast_addop_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.Add(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [90, 91, Bytecode.ADD]

def test_ast_subtractop_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.Subtract(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [90, 91, Bytecode.SUB]

def test_ast_mulop_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.Multiply(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [90, 91, Bytecode.MUL]

def test_ast_divop_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.Divide(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [90, 91, Bytecode.DIV]

def test_ast_unarynot_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.UnaryNot(DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [90, Bytecode.NOT]

def test_ast_unarynegate_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)
    node = ast.UnaryNegate(DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [90, Bytecode.NEG]

def test_ast_whilestatement_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    # Add padding to bytecodes to test non-zero based context (this is more realistic)
    ctx.emit(100)
    node = ast.WhileStatement(DummyCompilationUnit(90), ast.Block([DummyCompilationUnit(91)]))
    node.accept(t)

    assert ctx.get_bytecode() == [100, 90, Bytecode.JUMP_IF_FALSE, 7, 91, Bytecode.JUMP, 1]

def test_ast_ifstatement_compiler():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    # Add padding to bytecodes to test non-zero based context (this is more realistic)
    ctx.emit(100)
    node = ast.IfStatement(DummyCompilationUnit(90), ast.Block([DummyCompilationUnit(91)]))
    node.accept(t)

    assert ctx.get_bytecode() == [100, 90, Bytecode.JUMP_IF_FALSE, 5, 91]

def test_ast_printstatement():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.PrintStatement(DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [90, Bytecode.PRINT]

def test_ast_functionstatement():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.FunctionStatement('a', ast.ParameterList(['a']), ast.Block([DummyCompilationUnit(90)]))
    node.accept(t)

    assert ctx.get_bytecode() == [Bytecode.LOAD_CONST, 0]
    assert len(ctx.inner_contexts) == 1
    assert ctx.inner_contexts[0].get_bytecode() == [90, Bytecode.HALT]
    assert ctx.inner_contexts[0].has_local('a') == True
    assert ctx.inner_contexts[0].get_parameter_count() == 1

def test_ast_functionexpression():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.FunctionExpression(ast.ParameterList(['a']), ast.Block([ast.ReturnStatement(ast.IdentifierExpression('a'))]))
    node.accept(t)

    assert ctx.get_bytecode() == [Bytecode.LOAD_CONST, 0]
    assert len(ctx.inner_contexts) == 1
    assert ctx.inner_contexts[0].get_bytecode() == [Bytecode.LOAD, 0, Bytecode.RETURN, Bytecode.HALT]
    assert ctx.inner_contexts[0].has_local('a') == True
    assert ctx.inner_contexts[0].get_parameter_count() == 1

def test_ast_functioncall():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.FunctionCall('a', ast.ArgumentList([DummyCompilationUnit(90), DummyCompilationUnit(91)]))
    node.accept(t)

    assert ctx.get_bytecode() == [90, 91, Bytecode.INVOKE, 0]

def test_ast_asyncfunctioncall():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.AsyncFunctionCall('a', ast.ArgumentList([DummyCompilationUnit(90), DummyCompilationUnit(91)]))
    node.accept(t)

    assert ctx.get_bytecode() == [90, 91, Bytecode.INVOKE_ASYNC, 0]

def test_ast_returnstatement():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.ReturnStatement(DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [90, Bytecode.RETURN]

def test_array_access():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.ArrayAccess(DummyCompilationUnit(90), DummyCompilationUnit(91))
    node.accept(t)

    assert ctx.get_bytecode() == [90, 91, Bytecode.ARRAY_LOAD]

def test_array_access_assignment():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.ArrayAssignment(ast.ArrayAccess(DummyCompilationUnit(90), DummyCompilationUnit(91)), DummyCompilationUnit(93))
    node.accept(t)

    assert ctx.get_bytecode() == [90, 91, 93, Bytecode.ARRAY_STORE]

def test_invoke_global_list():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.FunctionCall('list', ast.ArgumentList([ast.IntegerConstant(10)]))
    node.accept(t)

    assert ctx.get_bytecode() == [Bytecode.LOAD_CONST, 0, Bytecode.INVOKE_GLOBAL, 0]

def test_break_statement():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.WhileStatement(DummyCompilationUnit(90), ast.Block([ast.BreakStatement()]))
    node.accept(t)

    assert ctx.get_bytecode() == [
            90,
            Bytecode.JUMP_IF_FALSE, 7,
            Bytecode.JUMP, 7,
            Bytecode.JUMP, 0
        ]

def test_continue_statement():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.WhileStatement(DummyCompilationUnit(90), ast.Block([ast.ContinueStatement()]))
    node.accept(t)

    assert ctx.get_bytecode() == [
            90,
            Bytecode.JUMP_IF_FALSE, 7,
            Bytecode.JUMP, 0,
            Bytecode.JUMP, 0
        ]

def test_channel_out():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.ChannelOut(DummyCompilationUnit(90))
    node.accept(t)

    assert ctx.get_bytecode() == [
            90,
            Bytecode.CHAN_OUT,
        ]

def test_channel_in():
    ctx = create_interpreter_context()
    t = create_syntax_directed_translator(ctx)

    node = ast.ChannelIn(DummyCompilationUnit(90), ast.Multiply(ast.IntegerConstant(10), ast.IntegerConstant(10)))
    node.accept(t)

    assert ctx.get_bytecode() == [
            90,
            Bytecode.LOAD_CONST, 0,
            Bytecode.LOAD_CONST, 0,
            Bytecode.MUL,
            Bytecode.CHAN_IN,
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
    assert ctx.literals[0] == Integer(10)

    # Outer context loads the function expression constant from literals area 0
    assert ctx.get_bytecode() == [
            Bytecode.LOAD_CONST, 0,  # Push the constant at 0 onto the stack (10)
            Bytecode.STORE, 0,       # Store the top of the stack into locals aread at 0
            Bytecode.LOAD_CONST, 1   # Push the function expression onto the top of the stack
        ]

    # Expect the constant to be stored in the literals area at position 0
    # Of the first inner method context
    inner_contexts = ctx.get_inner_contexts()
    assert len(inner_contexts) == 1
    assert inner_contexts[0].literals[0] == Integer(12)

    assert inner_contexts[0].get_bytecode() == [
            Bytecode.LOAD_CONST, 0,            # Push 12 onto the stack
            Bytecode.STORE_DYNAMIC, 0, 1, # Store 12 into the dynamic variable x
            Bytecode.LOAD_DYNAMIC, 0, 1,  # Load dynamic variable x onto the top of the stack
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
                        ast.Add(
                            ast.Multiply(
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
                ast.ArgumentList([ast.IntegerConstant(2)])
            ),
            ast.FunctionCall(
                'a',
                ast.ArgumentList([ast.IntegerConstant(4)])
            )
        ])

    node.accept(t)

    assert ctx.get_bytecode() == [
            Bytecode.LOAD_CONST, 0,
            Bytecode.STORE, 0,
            Bytecode.LOAD_CONST, 1,
            Bytecode.STORE, 1,
            Bytecode.LOAD_CONST, 2,
            Bytecode.INVOKE, 1,
            Bytecode.LOAD_CONST, 3,
            Bytecode.INVOKE, 1,
    ]

    inner_contexts = ctx.get_inner_contexts()

    assert inner_contexts[0].get_bytecode() == [
        Bytecode.LOAD_DYNAMIC, 0, 1,
        Bytecode.LOAD_CONST, 0,
        Bytecode.LOAD, 0,
        Bytecode.MUL,
        Bytecode.ADD,
        Bytecode.PRINT,
        Bytecode.HALT
    ]
