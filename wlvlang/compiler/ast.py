from rpython.rlib.parsing.tree import Symbol
from wlvlang.interpreter.bytecode import Bytecode

class Node:
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self == other

    def accept(self, astvisitor):
        pass

class Block(Node):
    def __init__(self, statements):
        self._statements = statements

    def accept(self, astvisitor):
        if astvisitor.visit_block(self):
            for statement in self._statements:
                statement.accept(astvisitor)

    def __repr__(self):
        return "Block(%r)" % (self._statements)

class BooleanConstant(Node):

    def __init__(self, value):
        self._value = value

    def accept(self, astvisitor):
        astvisitor.visit_booleanconstant(self)

    def __repr__(self):
        return "BooleanConstant(%r)" % (self._value)

class StringConstant(Node):

    def __init__(self, value):
        self._value = value

    def accept(self, astvisitor):
        astvisitor.visit_stringconstant(self)

    def __repr__(self):
        return "StringConstant(%s)" % (self._value)

class IntegerConstant(Node):

    def __init__(self, value):
        self._value = value

    def accept(self, astvisitor):
        astvisitor.visit_integerconstant(self)

    def __repr__(self):
        return "IntegerConstant(%d)" % (self._value)

class FloatConstant(Node):
    def __init__(self, value):
        self._value = value

    def accept(self, astvisitor):
        astvisitor.visit_floatconstant(self)

    def __repr__(self):
        return "FloatConstant(%r)" % self._value

class Assignment(Node):

    def __init__(self, variable_name, expression):
        self._varname = variable_name
        self._expression = expression

    def accept(self, astvisitor):
        if astvisitor.visit_assignment(self):
            self._expression.accept(astvisitor)

    def __repr__(self):
        return "Assignment(%r, %r)" % (self._varname, self._expression)

class Or(Node):

    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def accept(self, astvisitor):
        if astvisitor.visit_or(self):
            self._lhs.accept(astvisitor)
            self._rhs.accept(astvisitor)

    def __repr__(self):
        return "Or(%r, %r)" % (self._lhs, self._rhs)

class And(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def accept(self, astvisitor):
        if astvisitor.visit_and(self):
            self._lhs.accept(astvisitor)
            self._rhs.accept(astvisitor)

    def __repr__(self):
        return "And(%r, %r)" % (self._lhs, self._rhs)

class Equals(Node):

    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def accept(self, astvisitor):
        if astvisitor.visit_equals(self):
            self._lhs.accept(astvisitor)
            self._rhs.accept(astvisitor)

    def __repr__(self):
        return "Equals(%r, %r)" % (self._lhs, self._rhs)

class NotEquals(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def accept(self, astvisitor):
        if astvisitor.visit_notequals(self):
            self._lhs.accept(astvisitor)
            self._rhs.accept(astvisitor)

    def __repr__(self):
        return "NotEquals(%r, %r)" % (self._lhs, self._rhs)

class LessThan(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def accept(self, astvisitor):
        if astvisitor.visit_lessthan(self):
            self._lhs.accept(astvisitor)
            self._rhs.accept(astvisitor)

    def __repr__(self):
        return "LessThan(%r, %r)" % ((self._lhs), (self._rhs))

class LessThanOrEqual(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def accept(self, astvisitor):
        if astvisitor.visit_lessthanorequal(self):
            self._lhs.accept(astvisitor)
            self._rhs.accept(astvisitor)

    def __repr__(self):
        return "LessThanOrEqual(%r, %r)" % ((self._lhs), (self._rhs))

class GreaterThan(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def accept(self, astvisitor):
        if astvisitor.visit_greaterthan(self):
            self._lhs.accept(astvisitor)
            self._rhs.accept(astvisitor)

    def __repr__(self):
        return "GreaterThan(%r, %r)" % ((self._lhs), (self._rhs))

class GreaterThanOrEqual(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def accept(self, astvisitor):
        if astvisitor.visit_greaterthanorequal(self):
            self._lhs.accept(astvisitor)
            self._rhs.accept(astvisitor)

    def __repr__(self):
        return "GreaterThanOrEqual(%r, %r)" % ((self._lhs), (self._rhs))

class AddOp(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def accept(self, astvisitor):
        if astvisitor.visit_addop(self):
            self._lhs.accept(astvisitor)
            self._rhs.accept(astvisitor)

    def __repr__(self):
        return "AddOp(%r, %r)" % ((self._lhs), (self._rhs))

class SubtractOp(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def accept(self, astvisitor):
        if astvisitor.visit_subtractop(self):
            self._lhs.accept(astvisitor)
            self._rhs.accept(astvisitor)

    def __repr__(self):
        return "SubtractOp(%r, %r)" % ((self._lhs), (self._rhs))

class MulOp(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def accept(self, astvisitor):
        if astvisitor.visit_mulop(self):
            self._lhs.accept(astvisitor)
            self._rhs.accept(astvisitor)

    def __repr__(self):
        return "MulOp(%r, %r)" % ((self._lhs), (self._rhs))

class DivOp(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def accept(self, astvisitor):
        if astvisitor.visit_divop(self):
            self._lhs.accept(astvisitor)
            self._rhs.accept(astvisitor)

    def __repr__(self):
        return "DivOp(%r, %r)" % ((self._lhs), (self._rhs))

class UnaryNot(Node):
    def __init__(self, expression):
        self._expression = expression

    def accept(self, astvisitor):
        if astvisitor.visit_unarynot(self):
            self._expression.accept(astvisitor)

    def __repr__(self):
        return "UnaryNot(%r)" % ((self._expression))

class UnaryNegate(Node):
    def __init__(self, expression):
        self._expression = expression

    def accept(self, astvisitor):
        if astvisitor.visit_unarynegate(self):
            self._expression.accept(astvisitor)

    def __repr__(self):
        return "UnaryNegate(%r)" % ((self._expression))

class WhileStatement(Node):

    def __init__(self, condition, block):
        self._condition = condition
        self._block = block

    def accept(self, astvisitor):
        if astvisitor.visit_whilestatement(self):
            self._condition.accept(astvisitor)
            self._block.accept(astvisitor)

    def __repr__(self):
        return "WhileStatement(condition=%r, block=%r)" % ((self._condition), (self._block))

class IfStatement(Node):
    def __init__(self, condition, block):
        self._condition = condition
        self._block = block

    def accept(self, astvisitor):
        if astvisitor.visit_ifstatement(self):
            self._condition.accept(astvisitor)
            self._block.accept(astvisitor)

    def __repr__(self):
        return "IfStatement(condition=%r, block=%r)" % ((self._condition), (self._block))

class PrintStatement(Node):
    def __init__(self, expression):
        self._expression = expression

    def accept(self, astvisitor):
        if astvisitor.visit_printstatement(self):
            self._expression.accept(astvisitor)

    def __repr__(self):
        return "PrintStatement(%r)" % ((self._condition))

class FunctionStatement(Node):
    def __init__(self, paramlist, block):
        self._paramlist = paramlist
        self._block = block

    def accept(self, astvisitor):
        if astvisitor.visit_functionstatement(self):
            self._block.accept(astvisitor)

    def __repr__(self):
        return "FunctionStatement(%r, %r)" % (self._paramlist, self._block)

class FunctionCall(Node):
    def __init__(self, identifier, arglist):
        self._identifier = identifier
        self._arglist = arglist

    def accept(self, astvisitor):
        if astvisitor.visit_functioncall(self):
            for arg in self._arglist:
                arg.accept(astvisitor)

    def __repr__(self):
        return "FunctionCall(%r, %r)" % (self._identifier, self._arglist)

class ReturnStatement(Node):
    def __init__(self, statement):
        self._statement = statement

    def accept(self, astvisitor):
        if astvisitor.visit_returnstatement(self):
            self._statement.accept(astvisitor)

    def __repr__(self):
        return "ReturnStatement(%r)" % self._statement

class IdentifierExpression(Node):
    def __init__(self, identifier):
        self._identifier = identifier

    def accept(self, astvisitor):
        astvisitor.visit_identifierexpression(self)

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

        operator = node.children[1].children[0].children[0].additional_info

        if operator == "*":
            return MulOp(self.visit_unary(node.children[0]), self.visit_term(node.children[1].children[1]))

        if operator == "/":
            return MulOp(self.visit_unary(node.children[0]), self.visit_term(node.children[1].children[1]))

        raise TypeError("Failed to parse a multitive expression")

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



class ASTVisitor(object):
    """ Base class for any AST visitor implementation. """
    def visit_block(self, node):
        return True

    def visit_booleanconstant(self, node):
        return True

    def visit_stringconstant(self, node):
        return True

    def visit_integerconstant(self, node):
        return True

    def visit_floatconstant(self, node):
        return True

    def visit_assignment(self, node):
        return True

    def visit_or(self, node):
        return True

    def visit_and(self, node):
        return True

    def visit_equals(self, node):
        return True

    def visit_notequals(self, node):
        return True

    def visit_lessthan(self, node):
        return True

    def visit_lessthanorequal(self, node):
        return True

    def visit_greaterthan(self, node):
        return True

    def visit_greaterthanorequal(self, node):
        return True

    def visit_addop(self, node):
        return True

    def visit_subtractop(self, node):
        return True

    def visit_mulop(self, node):
        return True

    def visit_divop(self, node):
        return True

    def visit_unarynot(self, node):
        return True

    def visit_unarynegate(self, node):
        return True

    def visit_whilestatement(self, node):
        return True

    def visit_ifstatement(self, node):
        return True

    def visit_printstatement(self, node):
        return True

    def visit_functionstatement(self, node):
        return True

    def visit_functioncall(self, node):
        return True

    def visit_returnstatement(self, node):
        return True

    def visit_identifier(self, node):
        return True

