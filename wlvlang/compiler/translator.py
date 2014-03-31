from wlvlang.compiler.context import FunctionCompilerContext
from wlvlang.compiler import ast
from wlvlang.compiler.error import CompilerException

from wlvlang.interpreter.bytecode import Bytecode
from wlvlang.interpreter.objectspace.primitives.builtin_definitions import builtin_functions

_builtin_functions = builtin_functions()

class SyntaxDirectedTranslator(ast.ASTVisitor):

    def __init__(self, compiler_context):
        self.context = compiler_context

    def visit_booleanconstant(self, node):
        boolean = self.context.space.new_boolean(node.get_boolean_value())
        self.context.emit(Bytecode.LOAD_CONST, self.context.register_literal(boolean))
        return True

    def visit_integerconstant(self, node):
        integer = self.context.space.new_integer(node.get_integer_constant())
        self.context.emit(Bytecode.LOAD_CONST, self.context.register_literal(integer))
        return True

    def visit_stringconstant(self, node):
        string = self.context.space.new_string(node.get_string_value())
        self.context.emit(Bytecode.LOAD_CONST, self.context.register_literal(string))
        return True

    def visit_assignment(self, node):

        if self.context.has_local(node.get_varname()):
            local = self.context.register_local(node.get_varname())
            node.expression.accept(self)
            self.context.emit(Bytecode.STORE, local)
        else:
            slot, level = self.context.register_dynamic(node.get_varname())
            if slot is FunctionCompilerContext.REGISTER_DYNAMIC_FAILED:
                raise CompilerException("'%s' has not been defined in this scope. You should use `let %s = ...` to initialise a variable" % (node.get_varname(), node.get_varname()), node.getsourcepos())

            node.expression.accept(self)
            self.context.emit(Bytecode.STORE_DYNAMIC, slot)
            self.context.emit(level)

        return False

    def visit_or(self, node):
        node.lhs.accept(self)
        node.rhs.accept(self)
        self.context.emit(Bytecode.OR)
        return False

    def visit_and(self, node):
        node.lhs.accept(self)
        node.rhs.accept(self)
        self.context.emit(Bytecode.AND)
        return False

    def visit_equals(self, node):
        node.lhs.accept(self)
        node.rhs.accept(self)
        self.context.emit(Bytecode.EQUAL)
        return False

    def visit_notequals(self, node):
        node.lhs.accept(self)
        node.rhs.accept(self)
        self.context.emit(Bytecode.NOT_EQUAL)
        return False

    def visit_lessthan(self, node):
        node.lhs.accept(self)
        node.rhs.accept(self)
        self.context.emit(Bytecode.LESS_THAN)
        return False

    def visit_lessthanorequal(self, node):
        node.lhs.accept(self)
        node.rhs.accept(self)
        self.context.emit(Bytecode.LESS_THAN_EQ)
        return False

    def visit_greaterthan(self, node):
        node.lhs.accept(self)
        node.rhs.accept(self)
        self.context.emit(Bytecode.GREATER_THAN)
        return False

    def visit_greaterthanorequal(self, node):
        node.lhs.accept(self)
        node.rhs.accept(self)
        self.context.emit(Bytecode.GREATER_THAN_EQ)
        return False

    def visit_add(self, node):
        node.rhs.accept(self)
        node.lhs.accept(self)
        self.context.emit(Bytecode.ADD)
        return False

    def visit_subtract(self, node):
        node.rhs.accept(self)
        node.lhs.accept(self)
        self.context.emit(Bytecode.SUB)
        return False

    def visit_multiply(self, node):
        node.rhs.accept(self)
        node.lhs.accept(self)
        self.context.emit(Bytecode.MUL)
        return False

    def visit_divide(self, node):
        node.rhs.accept(self)
        node.lhs.accept(self)
        self.context.emit(Bytecode.DIV)
        return False

    def visit_mod(self, node):
        node.rhs.accept(self)
        node.lhs.accept(self)
        self.context.emit(Bytecode.MOD)
        return False


    def visit_unarynot(self, node):
        node.expression.accept(self)
        self.context.emit(Bytecode.NOT)
        return False

    def visit_unarynegate(self, node):
        node.expression.accept(self)
        self.context.emit(Bytecode.NEG)
        return False

    def visit_breakstatement(self, node):
        loop_control = self.context.peek_loop_control()
        self.context.emit(Bytecode.JUMP, loop_control[1])
        return True

    def visit_continuestatement(self, node):
        loop_control = self.context.peek_loop_control()
        self.context.emit(Bytecode.JUMP, loop_control[0])
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
        self.context.emit(Bytecode.JUMP_IF_FALSE, label_end)

        # Evaluate block
        node.block.accept(self)

        # Loop block so remove loop control labels from stack
        self.context.pop_loop_control()

        # Emit a GOTO to actually loop
        self.context.emit(Bytecode.JUMP, label_start)

        # Now we know what the value of the end label should be set it.
        self.context.set_label(label_end, self.context.get_top_position() + 1)
        return False

    def visit_ifstatement(self, node):
        node.condition.accept(self)
        endlabel = self.context.add_label()
        self.context.emit(Bytecode.JUMP_IF_FALSE, endlabel)
        node.ifclause.accept(self)
        self.context.set_label(endlabel, self.context.get_top_position() + 1)
        return False

    def visit_printstatement(self, node):
        node.expression.accept(self)
        self.context.emit(Bytecode.PRINT)
        return False

    def visit_functionstatement(self, node):
        raise NotImplementedError()

    def visit_functionexpression(self, node):
        new_context = FunctionCompilerContext(self.context.space, outer=self.context)
        self.context.add_inner_context(new_context)

        parameters = node.get_parameterlist().get_parameter_list()
        parameter_count = len(parameters)

        for param in parameters:
            new_context.register_local(param)

        new_context.set_parameter_count(parameter_count)
        new_visitor = SyntaxDirectedTranslator(new_context)
        node.block.accept(new_visitor)
        new_context.emit(Bytecode.HALT)
        method = new_context.generate_method()
        self.context.emit(Bytecode.LOAD_CONST, self.context.register_literal(method))
        return False

    def visit_asyncfunctioncall(self, node):
        for arg in node.get_arguments().get_argument_list():
            arg.accept(self)

        if node.identifier.get_identifier() in _builtin_functions:
            raise CompilerException("Built in functions can not be called with the async modifier", node.getsourcepos())

        node.identifier.accept(self)
        self.context.emit(Bytecode.INVOKE_ASYNC)

        return False

    def visit_functioncall(self, node):
        for arg in node.get_arguments().get_argument_list():
            arg.accept(self)

        if node.identifier.get_identifier() in _builtin_functions:
            function = _builtin_functions[node.identifier.get_identifier()]
            self.context.emit(Bytecode.INVOKE_GLOBAL, function[1])
        else:
            node.identifier.accept(self)
            self.context.emit(Bytecode.INVOKE)

        return False

    def visit_returnstatement(self, node):
        if node.expression is not None:
            node.expression.accept(self)
            self.context.emit(Bytecode.RETURN)
        else:
            self.context.emit(Bytecode.HALT)

        return False

    def visit_identifierexpression(self, node):

        if self.context.has_local(node.identifier):
            local = self.context.register_local(node.identifier)
            self.context.emit(Bytecode.LOAD, local)
        else:
            slot, level = self.context.register_dynamic(node.identifier)
            if slot == FunctionCompilerContext.REGISTER_DYNAMIC_FAILED:
                raise CompilerException("'%s' has not been defined in any scope. You should use `let %s = ...` to initialise a variable" % (node.identifier, node.identifier), node.getsourcepos())
            self.context.emit(Bytecode.LOAD_DYNAMIC, slot)
            self.context.emit(level)

        return True

    def visit_arrayaccess(self, node):
        node.identifier.accept(self)
        node.index.accept(self)
        self.context.emit(Bytecode.ARRAY_LOAD)
        return False

    def visit_arrayassignment(self, node):
        assert isinstance(node, ast.ArrayAssignment)  # RPython
        node.get_array_access().get_identifier().accept(self)
        node.array_access.index.accept(self)
        node.expression.accept(self)
        self.context.emit(Bytecode.ARRAY_STORE)
        return False

    def visit_scopedassignment(self, node):
        local = self.context.register_local(node.varname)
        node.expression.accept(self)
        self.context.emit(Bytecode.STORE, local)
        return False

    def visit_channelout(self, node):
        node.channel.accept(self)
        self.context.emit(Bytecode.CHAN_OUT)
        return False

    def visit_channelin(self, node):
        node.get_channel().accept(self)
        node.get_expression().accept(self)
        self.context.emit(Bytecode.CHAN_IN)
