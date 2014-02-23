from rply.token import BaseBox

class Node(BaseBox):
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self == other

    def accept(self, astvisitor):
        pass

class Block(Node):
    def __init__(self, statement_list):
        self._statements = statement_list

    def get_statements(self):
        return self._statements

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
        return "FloatConstant(%r)" % (self._value)

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

class ModOp(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def accept(self, astvisitor):
        if astvisitor.visit_modop(self):
            self._lhs.accept(astvisitor)
            self._rhs.accept(astvisitor)

    def __repr__(self):
        return "ModOp(%r, %r)" % ((self._lhs), (self._rhs))

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
        assert isinstance(condition, Node)
        self.condition = condition
        self.block = block

    def accept(self, astvisitor):
        if astvisitor.visit_whilestatement(self):
            self.condition.accept(astvisitor)
            self.block.accept(astvisitor)

    def __repr__(self):
        return "WhileStatement(condition=%r, block=%r)" % ((self.condition), (self.block))

class IfStatement(Node):
    def __init__(self, condition, ifclause):
        self.condition = condition
        self.ifclause = ifclause

    def accept(self, astvisitor):
        if astvisitor.visit_ifstatement(self):
            self.condition.accept(astvisitor)
            self.ifclause.accept(astvisitor)

    def __repr__(self):
        return "IfStatement(condition=%r, ifclause=%r)" % (self.condition, self.ifclause)

class PrintStatement(Node):
    def __init__(self, statement):
        self.statement = statement

    def accept(self, astvisitor):
        if astvisitor.visit_printstatement(self):
            self.statement.accept(astvisitor)

    def __repr__(self):
        return "PrintStatement(%r)" % self.statement

class ParameterList(Node):
    def __init__(self, parameters):
        self.parameters = parameters

    def get_parameters(self):
        return self.parameters

    def accept(self, astvisitor):
        astvisitor.visit_paramlist(self)

    def __repr__(self):
        return "ParameterList(%r)" % self.parameters

class FunctionExpression(Node):
    def __init__(self, paramlist, block):
        self.paramlist = paramlist
        self.block = block

    def get_parameters(self):
        return self.paramlist.get_parameters()

    def accept(self, astvisitor):
        if astvisitor.visit_functionexpression(self):
            self.block.accept(astvisitor)

    def __repr__(self):
        return "FunctionExpression(paramlist=%r, block=%r)" % (self.paramlist, self.block)

class FunctionStatement(Node):
    def __init__(self, identifier, paramlist, block):
        self.identifier = identifier
        self._paramlist = paramlist
        self._block = block

    def get_parameters(self):
        return self._paramlist.get_parameters()

    def accept(self, astvisitor):
        if astvisitor.visit_functionstatement(self):
            self._block.accept(astvisitor)

    def __repr__(self):
        return "FunctionStatement(%r, %r, %r)" % (self.identifier, self._paramlist, self._block)

class FunctionCall(Node):
    def __init__(self, identifier, arglist):
        self._identifier = identifier
        self._arglist = arglist

    def get_arguments(self):
        return self._arglist.get_arguments()

    def get_identifier(self):
        return self._identifier

    def accept(self, astvisitor):
        if astvisitor.visit_functioncall(self):
            for arg in self.get_arguments():
                arg.accept(astvisitor)

    def __repr__(self):
        return "FunctionCall(%r, %r)" % (self._identifier, self._arglist)

class FunctionArgList(Node):
    def __init__(self, arglist):
        self.arguments = arglist

    def get_arguments(self):
        return self.arguments

    def accept(self, astvisitor):
        if astvisitor.visit_arglist(self):
            for arg in self.arguments:
                arg.accept(astvisitor)

    def __repr__(self):
        return "FunctionArgList(%r)" % (self.arguments)

class ReturnStatement(Node):
    def __init__(self, statement):
        self._statement = statement

    def accept(self, astvisitor):
        if astvisitor.visit_returnstatement(self):
            self._statement.accept(astvisitor)

    def __repr__(self):
        return "ReturnStatement(%r)" % (self._statement)

class BreakStatement(Node):

    def __init__(self):
        pass

    def accept(self, astvisitor):
        astvisitor.visit_breakstatement(self)

    def __repr__(self):
        return "BreakStatement()"

class ContinueStatement(Node):

    def __init__(self):
        pass

    def accept(self, astvisitor):
        astvisitor.visit_continuestatement(self)

    def __repr__(self):
        return "ContinueStatement()"

class IdentifierExpression(Node):
    def __init__(self, identifier):
        self._identifier = identifier

    def accept(self, astvisitor):
        astvisitor.visit_identifierexpression(self)

    def __repr__(self):
        return "IdentifierExpression(%r)" % (self._identifier)

class ArrayAccess(Node):
    def __init__(self, identifier, index):
        self.identifier = identifier
        self.index = index

    def get_identifier(self):
        return self.identifier

    def get_index(self):
        return self.index

    def accept(self, astvisitor):
        if astvisitor.visit_arrayaccess(self):
            self.identifier.accept(astvisitor)
            self.index.accept(astvisitor)

    def __repr__(self):
        return "ArrayAccess()"

class ArrayAssignment(Node):

    def __init__(self, array_access, expression):
        assert isinstance(array_access, ArrayAccess)
        self.array_access = array_access
        self.expression = expression

    def get_array_access(self):
        return self.array_access

    def accept(self, astvisitor):
        if astvisitor.visit_arrayassignment(self):
            self.array_access.accept(astvisitor)
            self.expression.accept(astvisitor)

    def __repr__(self):
        return "ArrayAssignment"

class ScopedAssignment(Node):

    def __init__(self, variable_name, expression):
        self._varname = variable_name
        self._expression = expression

    def accept(self, astvisitor):
        if astvisitor.visit_scopedassignment(self):
            self._expression.accept(astvisitor)

    def __repr__(self):
        return "ScopedAssignment(%r, %r)" % (self._varname, self._expression)


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

    def visit_modop(self, node):
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

    def visit_functionexpression(self, node):
        return True

    def visit_functioncall(self, node):
        return True

    def visit_returnstatement(self, node):
        return True

    def visit_identifier(self, node):
        return True

    def visit_arglist(self, node):
        return True

    def visit_paramlist(self, node):
        return True

    def visit_arrayaccess(self, node):
        return True

    def visit_arrayassignment(self, node):
        return True

    def visit_scopedassignment(self, node):
        return True

    def visit_breakstatement(self, node):
        return True

    def visit_continuestatement(self, node):
        return True
