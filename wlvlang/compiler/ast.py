from rpython.rlib.parsing.tree import Symbol
from wlvlang.compiler.context import MethodCompilerContext
from wlvlang.interpreter.bytecode import Bytecode

class Node:
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self == other

    def compiler(self, context):
        pass

class Block(Node):
    def __init__(self, statements):
        self._statements = statements

    def compile(self, context):
        for statement in self._statements:
            statement.compile(context)

    def __repr__(self):
        return "Block(%r)" % (self._statements)


class Statement(Node):
    def __init__(self, expression):
        self._expression = expression

    def compiler(self, context):
        self._expression.compile(context)

    def __repr__(self):
        return "Statement(%r)" % (self._expression)

class BooleanConstant(Node):

    def __init__(self, value):
        self._value = value

    def compile(self, context):
        boolean = context.universe().new_boolean(self._value)
        context.emit(Bytecode.LOAD_CONST, context.register_literal(boolean))

    def __repr__(self):
        return "BooleanConstant(%r)" % (self._value)

class StringConstant(Node):

    def __init__(self, value):
        self._value = value

    def compile(self, context):
        pass

    def __repr__(self):
        return "StringConstant(%s)" % (self._value)

class IntegerConstant(Node):

    def __init__(self, value):
        self._value = value

    def compile(self, context):
        integer = context.universe().new_integer(self._value)
        context.emit(Bytecode.LOAD_CONST, context.register_literal(integer))

    def __repr__(self):
        return "IntegerConstant(%d)" % (self._value)

class FloatConstant(Node):
    def __init__(self, value):
        self._value = value

    def compile(self, context):
        pass

    def __repr__(self):
        return "FloatConstant(%r)" % self._value

class Assignment(Node):

    def __init__(self, variable_name, expression):
        self._varname = variable_name
        self._expression = expression

    def compile(self, context):
        local = context.register_local(self._varname)
        self._expression.compile(context)
        context.emit(Bytecode.STORE, local)

    def __repr__(self):
        return "Assignment(%r, %r)" % (self._varname, self._expression)

class Or(Node):

    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.OR)

    def __repr__(self):
        return "Or(%r, %r)" % (self._lhs, self._rhs)

class And(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.AND)

    def __repr__(self):
        return "And(%r, %r)" % (self._lhs, self._rhs)

class Equals(Node):

    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.EQUAL)

    def __repr__(self):
        return "Equals(%r, %r)" % (self._lhs, self._rhs)

class NotEquals(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.NOT_EQUAL)

    def __repr__(self):
        return "NotEquals(%r, %r)" % (self._lhs, self._rhs)

class LessThan(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.LESS_THAN)

    def __repr__(self):
        return "LessThan(%r, %r)" % ((self._lhs), (self._rhs))

class LessThanOrEqual(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.LESS_THAN_EQ)
    def __repr__(self):
        return "LessThanOrEqual(%r, %r)" % ((self._lhs), (self._rhs))

class GreaterThan(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.GREATER_THAN)

    def __repr__(self):
        return "GreaterThan(%r, %r)" % ((self._lhs), (self._rhs))

class GreaterThanOrEqual(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.GREATER_THAN_EQ)
    def __repr__(self):
        return "GreaterThanOrEqual(%r, %r)" % ((self._lhs), (self._rhs))

class AddOp(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.ADD)

    def __repr__(self):
        return "AddOp(%r, %r)" % ((self._lhs), (self._rhs))

class SubtractOp(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.SUB)

    def __repr__(self):
        return "SubtractOp(%r, %r)" % ((self._lhs), (self._rhs))

class MulOp(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.MUL)

    def __repr__(self):
        return "MulOp(%r, %r)" % ((self._lhs), (self._rhs))

class DivOp(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.DIV)

    def __repr__(self):
        return "DivOp(%r, %r)" % ((self._lhs), (self._rhs))

class UnaryNot(Node):
    def __init__(self, expression):
        self._expression = expression

    def compile(self, context):
        self._expression.compile(context)
        context.emit(Bytecode.NOT)

    def __repr__(self):
        return "UnaryNot(%r)" % ((self._expression))

class UnaryNegate(Node):
    def __init__(self, expression):
        self._expression = expression

    def compile(self, context):
        self._expression.compile(context)
        context.emit(Bytecode.NEG)

    def __repr__(self):
        return "UnaryNegate(%r)" % ((self._expression))

class WhileStatement(Node):

    def __init__(self, condition, block):
        self._condition = condition
        self._statements = block

    def compile(self, context):
        pos = len(context.bytecode)
        self._condition.compile(context)
        context.emit(Bytecode.JUMP_IF_FALSE, 0)
        jmp_back_to = len(context.bytecode) - 1
        self._statements.compile(context)
        context.emit(Bytecode.JUMP_BACK, pos)
        context.bytecode[jmp_back_to] = chr(len(context.bytecode))

    def __repr__(self):
        return "WhileStatement(condition=%r, block=%r)" % ((self._condition), (self._block))

class IfStatement(Node):
    def __init__(self, condition, block):
        self._condition = condition
        self._statements = block

    def compile(self, context):
        self._condition.compile(context)
        context.emit(Bytecode.JUMP_IF_FALSE, 0)
        position = len(context.data) - 1
        self._statements.compile(context)
        context.data[position] = chr(len(context.data))

    def __repr__(self):
        return "IfStatement(condition=%r, block=%r)" % ((self._condition), (self._block))

class PrintStatement(Node):
    def __init__(self, expression):
        self._expression = expression

    def compile(self, context):
        self._expression.compile(context)
        context.emit(Bytecode.PRINT)

    def __repr__(self):
        return "PrintStatement(%r)" % ((self._condition))

class FunctionStatement(Node):
    def __init__(self, paramlist, block):
        self._paramlist = paramlist
        self._block = block

    def compile(self, context):

        new_function_context = MethodCompilerContext(context.universe(), outer=context)
        for param in self._paramlist:
            new_function_context.register_local(param)

        self._block.compile(new_function_context)
        context.add_inner_context(new_function_context)
        method = new_function_context.generate_method()
        context.emit(Bytecode.LOAD_CONST, context.register_literal(method))

    def __repr__(self):
        return "FunctionStatement(%r, %r)" % (self._paramlist, self._block)

class FunctionCall(Node):
    def __init__(self, identifier, arglist):
        self._identifier = identifier
        self._arglist = arglist

    def compile(self, context):
        local = context.register_local(self._identifier)
        for argument in self._arglist:
            argument.compile(context)

        context.emit(Bytecode.INVOKE, local)

    def __repr__(self):
        return "FunctionCall(%r, %r)" % (self._identifier, self._arglist)

class ReturnStatement(Node):
    def __init__(self, statement):
        self._statement = statement

    def compile(self, context):
        self._statement.compile(context)
        context.emit(Bytecode.RETURN)

    def __repr__(self):
        return "ReturnStatement(%r)" % self._statement

class IdentifierExpression(Node):
    def __init__(self, identifier):
        self._identifier = identifier

    def compile(self, context):
        local = context.register_local(self._identifier)
        context.emit(Bytecode.LOAD, local)

    def __repr__(self):
        return "IdentifierExpression(%r)" % self._identifier

class Transformer(object):

    def _get_statements(self, kleene):
        statements = []

        while len(kleene.children) == 2:
            statements.append(self.visit_stmt(kleene.children[0]))
            kleene = kleene.children[1]

        statements.append(self.visit_stmt(kleene.children[0]))
        return Block(statements)

    def visit_program(self, node):
        statements = self._get_statements(node.children[0])
        return statements

    def visit_bool(self, node):
        if len(node.children) == 1:
            return self.visit_join(node.children[0])

        return Or(self.visit_join(node.children[0]), self.visit_bool(node.children[2]))

    def visit_join(self, node):
        if len(node.children) == 1:
            return self.visit_equality(node.children[0])

        return And(self.visit_equality(node.children[0]), self.visit_join(node.children[2]))

    def visit_equality(self, node):
        if len(node.children) == 1:
            return self.visit_relation(node.children[0])

        if node.children[1].additional_info == "==":
            return Equals(self.visit_relation(node.children[0]), self.visit_equality(node.children[2]))

        if node.children[1].additional_info == "!=":
            return NotEquals(self.visit_relation(node.children[0]), self.visit_equality(node.children[2]))

        raise TypeError("Failed to parse an equality expression")

    def visit_relation(self, node):
        if len(node.children) == 1:
            return self.visit_expr(node.children[0])

        if node.children[1].additional_info == "<":
            return LessThan(self.visit_expr(node.children[0]), self.visit_expr(node.children[2]))
        if node.children[1].additional_info == "<=":
            return LessThanOrEqual(self.visit_expr(node.children[0]), self.visit_expr(node.children[2]))
        if node.children[1].additional_info == ">":
            return GreaterThan(self.visit_expr(node.children[0]), self.visit_expr(node.children[2]))
        if node.children[1].additional_info == ">=":
            return GreaterThanOrEqual(self.visit_expr(node.children[0]), self.visit_expr(node.children[2]))

        raise TypeError("Failed to parse a relation expression")


    def visit_expr(self, node):
        if len(node.children) == 1:
            return self.visit_term(node.children[0])

        if node.children[1].additional_info == "+":
            return AddOp(self.visit_term(node.children[0]), self.visit_expr(node.children[2]))

        if node.children[1].additional_info == "-":
            return SubtractOp(self.visit_term(node.children[0]), self.visit_expr(node.children[2]))

        raise TypeError("Failed to parse an additive expression")

    def visit_term(self, node):
        if len(node.children) == 1:
            return self.visit_unary(node.children[0])

        if node.children[1].additional_info == "*":
            return MulOp(self.visit_unary(node.children[0]), self.visit_term(node.children[2]))
        if node.children[1].additional_info == "/":
            return DivOp(self.visit_unary(node.children[0]), self.visit_term(node.children[2]))

        raise TypeError("Failed to parse an multitive expression")

    def visit_unary(self, node):
        if len(node.children) == 1:
            return self.visit_factor(node.children[0])

        if node.children[0].additional_info == "not" or node.children[0].additional_info == "!":
            return UnaryNot(self.visit_unary(node.children[1]))

        if node.children[0].additional_info == "-":
            return UnaryNegate(self.visit_unary(node.children[1]))

        raise TypeError("Failed to parse an unary expression")

    def visit_factor(self, node):
        if len(node.children) == 1:
            return self.visit_atom(node.children[0])

        return self.visit_bool(node.children[1])

    def visit_atom(self, node):
        if node.children[0].symbol == "booleanliteral":
            return self.visit_booleanliteral(node.children[0])

        if node.children[0].symbol == "numericliteral":
            return self.visit_numericliteral(node.children[0])

        if node.children[0].symbol == "stringliteral":
            return self.visit_stringliteral(node.children[0])

        if node.children[0].symbol == "identifier":
            return self.visit_identifier(node.children[0])

        raise TypeError("Failed to parse an atom: %r" % node)


    def visit_booleanliteral(self, node):
        if node.children[0].additional_info == "true":
            return BooleanConstant(True)

        return BooleanConstant(False)

    def visit_numericliteral(self, node):
        if node.children[0].symbol == "FLOATLITERAL":
            return FloatConstant(float(node.children[0].additional_info))

        if node.children[0].symbol == "INTEGERLITERAL":
            # TODO: Convert string to bigint accordingly
            return IntegerConstant(int(node.children[0].additional_info))

    def visit_stringliteral(self, node):
        return StringConstant(node.children[0].additional_info)

    def visit_identifier(self, node):
        return IdentifierExpression(node.children[0].additional_info)

    def visit_fnstatement(self, node):
        paramlist = []

        if node.children[2].children[0].symbol == "paramlist":
            paramlist = self.visit_paramlist(node.children[2].children[0])
            block = self._get_statements(node.children[3].children[2])
        else:
            block = self._get_statements(node.children[2].children[2])

        return FunctionStatement(paramlist, block)

    def visit_paramlist(self, node):
        paramlist = []
        for identifier in node.children:
            paramlist.append(identifier.children[0].children[0].additional_info)
        return paramlist

    def visit_functioncall(self, node):
        identifier = node.children[0].children[0].additional_info
        if len(node.children) == 3:
            return FunctionCall(identifier, [])

        return FunctionCall(identifier, self.visit_arglist(node.children[2]))

    def visit_arglist(self, node):
        args = []
        for stmt in node.children[0].children[0].children:
            if isinstance(stmt, Symbol):
                continue

            if stmt.symbol != 'stmt':
                args.append(self.visit_stmt(stmt.children[0]))
            else:
                args.append(self.visit_stmt(stmt))

        if len(node.children[0].children) > 1:
            args.append(self.visit_stmt(node.children[0].children[1].children[0]))
        return args

    def visit_returnstmt(self, node):
        return ReturnStatement(self.visit_stmt(node.children[1]))

    def visit_stmt(self, node):

        if len(node.children) == 3 and node.children[1].additional_info == "=":
            # Normal assignment
            return Assignment(node.children[0].children[0].additional_info, self.visit_stmt(node.children[2]))

        if len(node.children) == 1:
            return self.visit_bool(node.children[0])

        if node.children[0].symbol == 'identifier':
            return self.visit_functioncall(node)

        if node.children[0].additional_info == 'fn':
            return self.visit_fnstatement(node)

        if node.children[0].additional_info == 'return':
            return self.visit_returnstmt(node)

        if node.children[0].additional_info == 'while':
            return WhileStatement(self.visit_stmt(node.children[2]), self._get_statements(node.children[5]))

        if node.children[0].additional_info == 'if':
            return IfStatement(self.visit_stmt(node.children[2]), self._get_statements(node.children[5]))

        if node.children[0].additional_info == 'print':
            return PrintStatement(self.visit_stmt(node.children[1]))
