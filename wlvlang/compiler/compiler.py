import os

from rpython.rlib.streamio import open_file_as_stream

from wlvlang.compiler.sourceparser import parse
from wlvlang.compiler.context import MethodCompilerContext
from wlvlang.interpreter.bytecode import Bytecode
from wlvlang.compiler.ast import ASTVisitor

from wlvlang.compiler.error import CompilerException

from wlvlang.vmobjects.primitives.primitives import primitive_functions

_primitive_functions = primitive_functions()

class SyntaxDirectedTranslator(ASTVisitor):

    def __init__(self, compiler_context):
        self._context = compiler_context

    def visit_booleanconstant(self, node):
        boolean = self._context.universe().new_boolean(node._value)
        self._context.emit(Bytecode.LOAD_CONST, self._context.register_literal(boolean))
        return True

    def visit_integerconstant(self, node):
        integer = self._context.universe().new_integer(node._value)
        self._context.emit(Bytecode.LOAD_CONST, self._context.register_literal(integer))
        return True

    def visit_assignment(self, node):
        node._expression.accept(self)

        if self._context.has_local(node._varname):
            local = self._context.register_local(node._varname)
            self._context.emit(Bytecode.STORE, local)
        else:
            slot, level = self._context.register_dynamic(node._varname)
            if slot is MethodCompilerContext.REGISTER_DYNAMIC_FAILED:
                raise CompilerException("Variable '%s' has not been defined in this scope. You should use `let %s = ...` to initialise a variable" % (node._varname, node._varname))
            self._context.emit(Bytecode.STORE_DYNAMIC, slot)
            self._context.emit(chr(level))

        return False

    def visit_or(self, node):
        node._lhs.accept(self)
        node._rhs.accept(self)
        self._context.emit(Bytecode.OR)
        return False

    def visit_and(self, node):
        node._lhs.accept(self)
        node._rhs.accept(self)
        self._context.emit(Bytecode.AND)
        return False

    def visit_equals(self, node):
        node._lhs.accept(self)
        node._rhs.accept(self)
        self._context.emit(Bytecode.EQUAL)
        return False

    def visit_notequals(self, node):
        node._lhs.accept(self)
        node._rhs.accept(self)
        self._context.emit(Bytecode.NOT_EQUAL)
        return False

    def visit_lessthan(self, node):
        node._lhs.accept(self)
        node._rhs.accept(self)
        self._context.emit(Bytecode.LESS_THAN)
        return False

    def visit_lessthanorequal(self, node):
        node._lhs.accept(self)
        node._rhs.accept(self)
        self._context.emit(Bytecode.LESS_THAN_EQ)
        return False

    def visit_greaterthan(self, node):
        node._lhs.accept(self)
        node._rhs.accept(self)
        self._context.emit(Bytecode.GREATER_THAN)
        return False

    def visit_greaterthanorequal(self, node):
        node._lhs.accept(self)
        node._rhs.accept(self)
        self._context.emit(Bytecode.GREATER_THAN_EQ)
        return False

    def visit_addop(self, node):
        node._lhs.accept(self)
        node._rhs.accept(self)
        self._context.emit(Bytecode.ADD)
        return False

    def visit_subtractop(self, node):
        node._lhs.accept(self)
        node._rhs.accept(self)
        self._context.emit(Bytecode.SUB)
        return False

    def visit_mulop(self, node):
        node._lhs.accept(self)
        node._rhs.accept(self)
        self._context.emit(Bytecode.MUL)
        return False

    def visit_divop(self, node):
        node._lhs.accept(self)
        node._rhs.accept(self)
        self._context.emit(Bytecode.DIV)
        return False

    def visit_unarynot(self, node):
        node._expression.accept(self)
        self._context.emit(Bytecode.NOT)
        return False

    def visit_unarynegate(self, node):
        node._expression.accept(self)
        self._context.emit(Bytecode.NEG)
        return False

    def visit_whilestatement(self, node):
        pos = len(self._context.bytecode)
        node.condition.accept(self)
        self._context.emit(Bytecode.JUMP_IF_FALSE, 0)
        jmp_forward_to = len(self._context.bytecode) - 1
        node.block.accept(self)
        self._context.emit(Bytecode.JUMP_BACK, pos)
        self._context.bytecode[jmp_forward_to] = chr(len(self._context.bytecode))
        return False

    def visit_ifstatement(self, node):
        node.condition.accept(self)
        self._context.emit(Bytecode.JUMP_IF_FALSE, 0)
        position = len(self._context.bytecode) - 1
        node.ifclause.accept(self)
        self._context.bytecode[position] = chr(len(self._context.bytecode))
        return False

    def visit_printstatement(self, node):
        node.statement.accept(self)
        self._context.emit(Bytecode.PRINT)
        return False

    def visit_functionstatement(self, node):
        new_context = MethodCompilerContext(self._context.universe(), outer=self._context)
        self._context.add_inner_context(new_context)
        parameters = node.get_parameters()
        parameter_count = len(parameters)
        for param in parameters:
            new_context.register_local(param)

        new_context.set_parameter_count(parameter_count)

        new_visitor = SyntaxDirectedTranslator(new_context)
        node._block.accept(new_visitor)
        new_context.emit(Bytecode.HALT)
        method = new_context.generate_method()
        self._context.emit(Bytecode.LOAD_CONST, self._context.register_literal(method))
        return False

    def visit_functionexpression(self, node):
        new_context = MethodCompilerContext(self._context.universe(), outer=self._context)
        self._context.add_inner_context(new_context)

        parameters = node.get_parameters()
        parameter_count = len(parameters)

        for param in parameters:
            new_context.register_local(param)

        new_context.set_parameter_count(parameter_count)
        new_visitor = SyntaxDirectedTranslator(new_context)
        node.block.accept(new_visitor)
        new_context.emit(Bytecode.HALT)
        method = new_context.generate_method()
        self._context.emit(Bytecode.LOAD_CONST, self._context.register_literal(method))
        return False

    def visit_functioncall(self, node):
        for arg in node.get_arguments():
            arg.accept(self)

        if node._identifier in _primitive_functions:
            function = _primitive_functions[node._identifier]
            self._context.emit(Bytecode.INVOKE_GLOBAL, function[1])
        else:
            local = self._context.register_local(node._identifier)
            self._context.emit(Bytecode.INVOKE, local)

        return False

    def visit_returnstatement(self, node):
        node._statement.accept(self)
        self._context.emit(Bytecode.RETURN)
        return False

    def visit_identifierexpression(self, node):

        if self._context.has_local(node._identifier):
            local = self._context.register_local(node._identifier)
            self._context.emit(Bytecode.LOAD, local)
        else:
            slot, level = self._context.register_dynamic(node._identifier)
            self._context.emit(Bytecode.LOAD_DYNAMIC, slot)
            self._context.emit(chr(level))

        return True

    def visit_arrayaccess(self, node):
        node.identifier.accept(self)
        node.index.accept(self)
        self._context.emit(Bytecode.ARRAY_LOAD)
        return False

    def visit_arrayassignment(self, node):
        node.array_access.identifier.accept(self)
        node.array_access.index.accept(self)
        node.expression.accept(self)
        self._context.emit(Bytecode.ARRAY_STORE)
        return False

    def visit_scopedassignment(self, node):
        local = self._context.register_local(node._varname)

        # TODO: Error checking
        node._expression.accept(self)
        self._context.emit(Bytecode.STORE, local)
        return False

def compile_source_from_file(path, filename, universe):
    """ Given a source file, return a vmobjects.Method object """
    fullname = path + os.sep + filename
    try:
        input_file = open_file_as_stream(fullname, "r")
        source = input_file.readall()

        try:
            ast = parse(source)
        except Exception, e:
            # TODO: Better errors
            os.write(2, "Failed to parse")
            # Raise something less specific here (as we output)
            raise e
        finally:
            input_file.close()
    except OSError, msg:
        os.write(2, "%s: %s\n" % (os.strerror(msg.errno), fullname))
        raise IOError()

    compiler_context = MethodCompilerContext(universe)
    sdt = SyntaxDirectedTranslator(compiler_context)
    ast.accept(sdt)
    compiler_context.emit(Bytecode.HALT)
    method = compiler_context.generate_method()
    return method
