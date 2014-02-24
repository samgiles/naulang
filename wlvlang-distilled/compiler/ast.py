import sys

from rply.token import BaseBox

class Node(BaseBox):
    """ Base ast Node """
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self == other

    def accept(self, astvisitor):
        """ Implements visitor pattern """
        pass

# Structure

class Block(Node):
    """ A Basic block or collection of Statements/Expressions """

    def __init__(self, statement_list):
        self.statements = statement_list

    def get_statements(self):
        return self.statements

    def accept(self, astvisitor):
        if astvisitor.visit_block(self):
            for statement in self.statements:
                statement.accept(astvisitor)

    def __repr__(self):
        return "ast.Block(%r)" % (self.statements)


# Constants

class BooleanConstant(Node):
    """ Represents a Boolean constant "true" or "false" """

    def __init__(self, value):
        self.value = value

    def get_boolean_value(self):
        return self.value

    def accept(self, astvisitor):
        astvisitor.visit_booleanconstant(self)

    def __repr__(self):
        return "ast.BooleanConstant(%r)" % (self.value)

class StringConstant(Node):
    """ Represents a String constant """

    def __init__(self, value):
        self.value = value

    def get_string_value(self):
        return self.value

    def accept(self, astvisitor):
        astvisitor.visit_stringconstant(self)

    def __repr__(self):
        return "ast.StringConstant(%s)" % (self.value)

class IntegerConstant(Node):
    """ Represents an Integer constant """

    def __init__(self, value):
        self.value = value

    def get_integer_constant(self):
        return self.value

    def accept(self, astvisitor):
        astvisitor.visit_integerconstant(self)

    def __repr__(self):
        return "ast.IntegerConstant(%d)" % (self.value)

class FloatConstant(Node):
    """ Represents a Floating point constant """

    def __init__(self, value):
        self.value = value

    def get_float_constant(self):
        return self.value

    def accept(self, astvisitor):
        astvisitor.visit_floatconstant(self)

    def __repr__(self):
        return "ast.FloatConstant(%r)" % (self.value)

# Statements

# # Assignment

class Assignment(Node):
    """ Represents simple assignment """

    def __init__(self, variable_name, expression):
        self.varname = variable_name
        self.expression = expression

    def get_varname(self):
        return self.varname

    def get_expression(self):
        return expression

    def accept(self, astvisitor):
        if astvisitor.visit_assignment(self):
            self.expression.accept(astvisitor)

    def __repr__(self):
        return "ast.Assignment(%r, %r)" % (self.varname, self.expression)

class ScopedAssignment(Node):
    """ Represents variable initialisation within a scope (using let keyword) """

    def __init__(self, variable_name, expression):
        self.varname = variable_name
        self.expression = expression

    def get_varname(self):
        return self.varname

    def get_expression(self):
        return self.expression

    def accept(self, astvisitor):
        if astvisitor.visit_scopedassignment(self):
            self.expression.accept(astvisitor)

    def __repr__(self):
        return "ast.ScopedAssignment(%r, %r)" % (self.varname, self.expression)

# Expressions

# # Logical

class Or(Node):
    """ Or Expression """

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def get_lhs(self):
        return self.lhs

    def get_rhs(self):
        return self.rhs

    def accept(self, astvisitor):
        if astvisitor.visit_or(self):
            self._lhs.accept(astvisitor)
            self._rhs.accept(astvisitor)

    def __repr__(self):
        return "ast.Or(%r, %r)" % (self.lhs, self.rhs)

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


def _visit(visitor, node):
    return True

def _create_visitor():
    """ NOT_RPYTHON

        Dynamically creates the ASTVisitor
    """
    import inspect
    import sys
    asts = inspect.getmembers(sys.modules[__name__], lambda obj: inspect.isclass(obj) and issubclass(obj, Node))
    for cls in asts:
        setattr(ASTVisitor, 'visit_' + cls.lower(), classmethod(_visit))

class ASTVisitor(object):
    pass

_create_visitor()
