import os

from rpython.rlib.streamio import open_file_as_stream
from rpython.rlib.parsing.parsing import ParseError

from wlvlang.compiler.sourceparser import parse
from wlvlang.compiler.context import MethodCompilerContext
from wlvlang.interpreter.bytecode import Bytecode
from wlvlang.compiler.ast import ASTVisitor


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
        local = self._context.register_local(node._varname)
        self._context.emit(Bytecode.STORE, local)
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
        node._condition.accept(self)
        self._context.emit(Bytecode.JUMP_IF_FALSE, 0)
        jmp_forward_to = len(self._context.bytecode) - 1
        node._block.accept(self)
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
        for param in node.get_parameters():
            new_context.register_local(param)

        new_visitor = SyntaxDirectedTranslator(new_context)
        node._block.accept(new_visitor)
        method = new_context.generate_method()
        self._context.emit(Bytecode.LOAD_CONST, self._context.register_literal(method))
        return False

    def visit_functioncall(self, node):
        local = self._context.register_local(node._identifier)

        for arg in node.get_arguments():
            arg.accept(self)

        self._context.emit(Bytecode.INVOKE, local)
        return False

    def visit_returnstatement(self, node):
        node._statement.accept(self)
        self._context.emit(Bytecode.RETURN)
        return False

    def visit_identifierexpression(self, node):
        local = self._context.register_local(node._identifier)
        self._context.emit(Bytecode.LOAD, local)
        return True


def compile_source_from_file(path, filename, universe):
    """ Given a source file, return a vmobjects.Method object """
    fullname = path + os.sep + filename
    try:
        input_file = open_file_as_stream(fullname, "r")
        source = input_file.readall()

        try:
            ast = parse(source)
        except ParseError, e:
            os.write(2, e.nice_error_message(filename=fullname, source=source))
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
