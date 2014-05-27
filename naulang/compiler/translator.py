from naulang.compiler.context import FunctionCompilerContext
from naulang.compiler import ast
from naulang.compiler.error import CompilerException

from naulang.interpreter.bytecode import Bytecode
from naulang.interpreter.objectspace.primitives.builtin_definitions import builtin_functions

_builtin_functions = builtin_functions()

class SyntaxDirectedTranslator(ast.ASTVisitor):
    """ Translate an AST to a function object graph.

        This doesn't emit pure bytecode, literals and symbol tables. Instead it
        uses the AST to build a tree of Method objects using the
        FunctionCompilerContext. Each time a function expression is encountered
        in the AST, a new FunctionCompilerContext is created and a new
        translator is created and invoked on the function subtree, this means
        the tree structure of the function defnitions is recursively translated
        into a tree of method objects.  Inner functions are stored as literals
        in its containing function to be referenced with LOAD_CONST bytecodes
        in the same way that all data is referenced. This allows us to use
        functions, as first class data types and gives rise to the 'lambda'
        style syntax of function composition:

            let f = fn(b, x) {
                return b(fn(y) {
                    return x + y
                })
            }

            print f(fn(x) {
                return x(10)
            }, 15)

        Output: 25  (the sum of 10 and 15 [in a somewhat contrived way])


        The translator would create 4 Method objects in this instance. One for
        the containing 'main' function.  One for the function assigned to f,
        within that function there is another that is used to pass into the
        function in 'b'.

        Another contained in the main function is the function that returns
        x(10). The structure created would look something like the following:

        [ MAIN ]
           |
           |------ fn(b,x) { ... }
           |          |
           |          |----- fn(y) { ... }
           |
           |------ fn(x) { ... }
    """

    def __init__(self, compiler_context):
        self.context = compiler_context

    def visit_booleanconstant(self, node):
        boolean = self.context.space.new_boolean(node.get_boolean_value())
        self.context.emit([Bytecode.LOAD_CONST, self.context.register_literal(boolean)], sourceposition=node.getsourcepos())
        return True

    def visit_integerconstant(self, node):
        integer = self.context.space.new_integer(node.get_integer_constant())
        self.context.emit([Bytecode.LOAD_CONST, self.context.register_literal(integer)], sourceposition=node.getsourcepos())
        return True

    def visit_floatconstant(self, node):
        float_val = self.context.space.new_float(node.get_float_constant())
        self.context.emit([Bytecode.LOAD_CONST, self.context.register_literal(float_val)], sourceposition=node.getsourcepos())

    def visit_stringconstant(self, node):
        string = self.context.space.new_string(node.get_string_value())
        self.context.emit([Bytecode.LOAD_CONST, self.context.register_literal(string)], sourceposition=node.getsourcepos())
        return True

    def visit_assignment(self, node):

        if self.context.has_local(node.get_varname()):
            local = self.context.register_local(node.get_varname())
            node.expression.accept(self)
            self.context.emit([Bytecode.STORE, local], sourceposition=node.getsourcepos())
        else:
            slot, level = self.context.register_dynamic(node.get_varname())
            if slot is FunctionCompilerContext.REGISTER_DYNAMIC_FAILED:
                raise CompilerException("'%s' has not been defined in this scope. You should use `let %s = ...` to initialise a variable" % (node.get_varname(), node.get_varname()), node.getsourcepos())

            node.expression.accept(self)
            self.context.emit([Bytecode.STORE_DYNAMIC, slot, level], sourceposition=node.getsourcepos())

        return False

    def visit_or(self, node):
        node.lhs.accept(self)
        node.rhs.accept(self)
        self.context.emit([Bytecode.OR], sourceposition=node.getsourcepos())
        return False

    def visit_and(self, node):
        node.lhs.accept(self)
        node.rhs.accept(self)
        self.context.emit([Bytecode.AND], sourceposition=node.getsourcepos())
        return False

    def visit_equals(self, node):
        node.lhs.accept(self)
        node.rhs.accept(self)
        self.context.emit([Bytecode.EQUAL], sourceposition=node.getsourcepos())
        return False


    def visit_notequals(self, node):
        node.lhs.accept(self)
        node.rhs.accept(self)
        self.context.emit([Bytecode.NOT_EQUAL], sourceposition=node.getsourcepos())
        return False

    def visit_lessthan(self, node):
        node.lhs.accept(self)
        node.rhs.accept(self)
        self.context.emit([Bytecode.LESS_THAN], sourceposition=node.getsourcepos())
        return False

    def visit_lessthanorequal(self, node):
        node.lhs.accept(self)
        node.rhs.accept(self)
        self.context.emit([Bytecode.LESS_THAN_EQ], sourceposition=node.getsourcepos())
        return False

    def visit_greaterthan(self, node):
        node.lhs.accept(self)
        node.rhs.accept(self)
        self.context.emit([Bytecode.GREATER_THAN], sourceposition=node.getsourcepos())
        return False

    def visit_greaterthanorequal(self, node):
        node.lhs.accept(self)
        node.rhs.accept(self)
        self.context.emit([Bytecode.GREATER_THAN_EQ], sourceposition=node.getsourcepos())
        return False

    def visit_add(self, node):
        node.rhs.accept(self)
        node.lhs.accept(self)
        self.context.emit([Bytecode.ADD], sourceposition=node.getsourcepos())
        return False

    def visit_subtract(self, node):
        node.rhs.accept(self)
        node.lhs.accept(self)
        self.context.emit([Bytecode.SUB], sourceposition=node.getsourcepos())
        return False

    def visit_multiply(self, node):
        node.rhs.accept(self)
        node.lhs.accept(self)
        self.context.emit([Bytecode.MUL], sourceposition=node.getsourcepos())
        return False

    def visit_divide(self, node):
        node.rhs.accept(self)
        node.lhs.accept(self)
        self.context.emit([Bytecode.DIV], sourceposition=node.getsourcepos())
        return False

    def visit_mod(self, node):
        node.rhs.accept(self)
        node.lhs.accept(self)
        self.context.emit([Bytecode.MOD], sourceposition=node.getsourcepos())
        return False


    def visit_unarynot(self, node):
        node.expression.accept(self)
        self.context.emit([Bytecode.NOT], sourceposition=node.getsourcepos())
        return False

    def visit_unarynegate(self, node):
        node.expression.accept(self)
        self.context.emit([Bytecode.NEG], sourceposition=node.getsourcepos())
        return False

    def visit_breakstatement(self, node):
        loop_control = self.context.peek_loop_control()
        self.context.emit([Bytecode.JUMP, loop_control[1]], sourceposition=node.getsourcepos())
        return True

    def visit_continuestatement(self, node):
        loop_control = self.context.peek_loop_control()
        self.context.emit([Bytecode.JUMP, loop_control[0]], sourceposition=node.getsourcepos())
        return True

    def visit_whilestatement(self, node):

        # Set up the labels for this while block and push them onto the loop control stack
        label_start = self.context.add_label(
                initial_value=self.context.get_top_position() + 1
            )

        label_end = self.context.add_label()

        self.context.push_loop_control(label_start, label_end)

        # Evaluate the condition and emit control instructions
        node.condition.accept(self)
        self.context.emit([Bytecode.JUMP_IF_FALSE, label_end], sourceposition=node.getsourcepos())

        # Evaluate block
        node.block.accept(self)

        # Loop block so remove loop control labels from stack
        self.context.pop_loop_control()

        # Emit a GOTO to actually loop
        self.context.emit([Bytecode.JUMP, label_start], sourceposition=node.getsourcepos())

        # Now we know what the value of the end label should be set it.
        self.context.set_label(label_end, self.context.get_top_position() + 1)
        return False

    def visit_ifstatement(self, node):
        node.condition.accept(self)
        endlabel = self.context.add_label()
        self.context.emit([Bytecode.JUMP_IF_FALSE, endlabel], sourceposition=node.getsourcepos())
        node.ifclause.accept(self)
        self.context.set_label(endlabel, self.context.get_top_position() + 1)
        return False

    def visit_printstatement(self, node):
        node.expression.accept(self)
        self.context.emit([Bytecode.PRINT], sourceposition=node.getsourcepos())
        return False

    def visit_functionstatement(self, node):
        raise NotImplementedError()

    def visit_functionexpression(self, node):
        new_context = FunctionCompilerContext(self.context.space, outer=self.context, optimise=self.context.should_optimise)
        self.context.add_inner_context(new_context)

        parameters = node.get_parameterlist().get_parameter_list()
        parameter_count = len(parameters)

        for param in parameters:
            new_context.register_local(param)

        new_context.set_parameter_count(parameter_count)
        new_visitor = SyntaxDirectedTranslator(new_context)
        if node.block is not None:
            node.block.accept(new_visitor)
        new_context.emit([Bytecode.HALT])
        method = new_context.generate_method()
        self.context.emit([Bytecode.LOAD_CONST, self.context.register_literal(method)], sourceposition=node.getsourcepos())
        return False

    def visit_asyncfunctioncall(self, node):
        for arg in node.get_arguments().get_argument_list():
            arg.accept(self)

        if node.identifier.get_identifier() in _builtin_functions:
            raise CompilerException("Built in functions can not be called with the async modifier", node.getsourcepos())

        node.identifier.accept(self)
        self.context.emit([Bytecode.INVOKE_ASYNC], sourceposition=node.getsourcepos())

        return False

    def visit_functioncall(self, node):
        for arg in node.get_arguments().get_argument_list():
            arg.accept(self)

        if node.identifier.get_identifier() in _builtin_functions:
            function = _builtin_functions[node.identifier.get_identifier()]
            self.context.emit([Bytecode.INVOKE_GLOBAL, function[1]], sourceposition=node.getsourcepos())
        else:
            node.identifier.accept(self)
            self.context.emit([Bytecode.INVOKE], sourceposition=node.getsourcepos())

        return False

    def visit_returnstatement(self, node):
        if node.expression is not None:
            node.expression.accept(self)
            self.context.emit([Bytecode.RETURN], sourceposition=node.getsourcepos())
        else:
            self.context.emit([Bytecode.HALT])

        return False

    def visit_identifierexpression(self, node):

        if self.context.has_local(node.identifier):
            local = self.context.register_local(node.identifier)
            self.context.emit([Bytecode.LOAD, local], sourceposition=node.getsourcepos())
        else:
            slot, level = self.context.register_dynamic(node.identifier)
            if slot == FunctionCompilerContext.REGISTER_DYNAMIC_FAILED:
                raise CompilerException("'%s' has not been defined in any scope. You should use `let %s = ...` to initialise a variable" % (node.identifier, node.identifier), node.getsourcepos())
            self.context.emit([Bytecode.LOAD_DYNAMIC, slot, level], sourceposition=node.getsourcepos())

        return True

    def visit_arrayaccess(self, node):
        node.identifier.accept(self)
        node.index.accept(self)
        self.context.emit([Bytecode.ARRAY_LOAD], sourceposition=node.getsourcepos())
        return False

    def visit_arrayassignment(self, node):
        assert isinstance(node, ast.ArrayAssignment)  # RPython
        node.get_array_access().get_identifier().accept(self)
        node.array_access.index.accept(self)
        node.expression.accept(self)
        self.context.emit([Bytecode.ARRAY_STORE], sourceposition=node.getsourcepos())
        return False

    def visit_scopedassignment(self, node):
        local = self.context.register_local(node.varname)
        node.expression.accept(self)
        self.context.emit([Bytecode.STORE, local], sourceposition=node.getsourcepos())
        return False

    def visit_channelout(self, node):
        node.channel.accept(self)
        self.context.emit([Bytecode.CHAN_OUT], sourceposition=node.getsourcepos())
        return False

    def visit_channelin(self, node):
        node.get_channel().accept(self)
        node.get_expression().accept(self)
        self.context.emit([Bytecode.CHAN_IN], sourceposition=node.getsourcepos())
