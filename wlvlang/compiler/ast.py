from rply.token import BaseBox

class Node(BaseBox):

    def __init__(self, sourceposition):
        self.sourceposition = sourceposition

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

    def __init__(self, statement_list, sourceposition):
        Node.__init__(self, sourceposition)
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

    def __init__(self, value, sourceposition):
        Node.__init__(self, sourceposition)
        self.value = value

    def get_boolean_value(self):
        return self.value

    def accept(self, astvisitor):
        astvisitor.visit_booleanconstant(self)

    def __repr__(self):
        return "ast.BooleanConstant(%r)" % (self.value)

class StringConstant(Node):
    """ Represents a String constant """

    def __init__(self, value, sourceposition):
        Node.__init__(self, sourceposition)
        self.value = value

    def get_string_value(self):
        return self.value

    def accept(self, astvisitor):
        astvisitor.visit_stringconstant(self)

    def __repr__(self):
        return "ast.StringConstant(%s)" % (self.value)

class IntegerConstant(Node):
    """ Represents an Integer constant """

    def __init__(self, value, sourceposition):
        Node.__init__(self, sourceposition)
        self.value = value

    def get_integer_constant(self):
        return self.value

    def accept(self, astvisitor):
        astvisitor.visit_integerconstant(self)

    def __repr__(self):
        return "ast.IntegerConstant(%d)" % (self.value)

class FloatConstant(Node):
    """ Represents a Floating point constant """

    def __init__(self, value, sourceposition):
        Node.__init__(self, sourceposition)
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

    def __init__(self, variable_name, expression, sourceposition):
        Node.__init__(self, sourceposition)
        self.varname = variable_name
        self.expression = expression

    def get_varname(self):
        return self.varname

    def get_expression(self):
        return self.expression

    def accept(self, astvisitor):
        if astvisitor.visit_assignment(self):
            self.expression.accept(astvisitor)

    def __repr__(self):
        return "ast.Assignment(%r, %r)" % (self.varname, self.expression)

class ScopedAssignment(Node):
    """ Represents variable initialisation within a scope (using let keyword) """

    def __init__(self, variable_name, expression, sourceposition):
        Node.__init__(self, sourceposition)
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

class BinaryExpression(Node):
    """ A generic Binary expression """
    def __init__(self, lhs, rhs, sourceposition):
        Node.__init__(self, sourceposition)
        self.lhs = lhs
        self.rhs = rhs

    def get_lhs(self):
        return self.lhs

    def get_rhs(self):
        return self.rhs

    def accept(self, astvisitor):
        if astvisitor.visit_binaryexpression(self):
            self.lhs.accept(astvisitor)
            self.rhs.accept(astvisitor)


# # Logical

class Or(BinaryExpression):
    """ Or Expression """

    def accept(self, astvisitor):
        if astvisitor.visit_or(self):
            BinaryExpression.accept(self, astvisitor)

    def __repr__(self):
        return "ast.Or(%r, %r)" % (self.lhs, self.rhs)

class And(BinaryExpression):
    """ And Expression """
    def accept(self, astvisitor):
        if astvisitor.visit_and(self):
            BinaryExpression.accept(self, astvisitor)

    def __repr__(self):
        return "ast.And(%r, %r)" % (self.lhs, self.rhs)

class Equals(BinaryExpression):
    """ Equals/Is expression; ==/is """

    def accept(self, astvisitor):
        if astvisitor.visit_equals(self):
            BinaryExpression.accept(self, astvisitor)

    def __repr__(self):
        return "ast.Equals(%r, %r)" % (self.lhs, self.rhs)

class NotEquals(BinaryExpression):
    """ Not equals expression; != """

    def accept(self, astvisitor):
        if astvisitor.visit_notequals(self):
            BinaryExpression.accept(self, astvisitor)

    def __repr__(self):
        return "ast.NotEquals(%r, %r)" % (self.lhs, self.rhs)

# # Relational

class LessThan(BinaryExpression):
    """ Less than expression; < """

    def accept(self, astvisitor):
        if astvisitor.visit_lessthan(self):
            BinaryExpression.accept(self, astvisitor)

    def __repr__(self):
        return "ast.LessThan(%r, %r)" % ((self.lhs), (self.rhs))

class LessThanOrEqual(BinaryExpression):
    """ Less than or equal; <= """

    def accept(self, astvisitor):
        if astvisitor.visit_lessthanorequal(self):
            BinaryExpression.accept(self, astvisitor)

    def __repr__(self):
        return "ast.LessThanOrEqual(%r, %r)" % ((self.lhs), (self.rhs))

class GreaterThan(BinaryExpression):
    """ Greater than; > """

    def accept(self, astvisitor):
        if astvisitor.visit_greaterthan(self):
            BinaryExpression.accept(self, astvisitor)

    def __repr__(self):
        return "ast.GreaterThan(%r, %r)" % ((self.lhs), (self.rhs))

class GreaterThanOrEqual(BinaryExpression):
    """ Greater than or equal; >= """

    def accept(self, astvisitor):
        if astvisitor.visit_greaterthanorequal(self):
            BinaryExpression.accept(self, astvisitor)

    def __repr__(self):
        return "ast.GreaterThanOrEqual(%r, %r)" % ((self.lhs), (self.rhs))

# # Arithmetic

class Add(BinaryExpression):
    """ Add; +.  Is concatenative if left hand side is string """

    def accept(self, astvisitor):
        if astvisitor.visit_add(self):
            BinaryExpression.accept(self, astvisitor)

    def __repr__(self):
        return "ast.AddOp(%r, %r)" % ((self.lhs), (self.rhs))

class Subtract(BinaryExpression):
    """ Subtract; -. """

    def accept(self, astvisitor):
        if astvisitor.visit_subtract(self):
            BinaryExpression.accept(self, astvisitor)

    def __repr__(self):
        return "ast.Subtract(%r, %r)" % ((self.lhs), (self.rhs))

class Multiply(BinaryExpression):
    """ Multiply; *. """

    def accept(self, astvisitor):
        if astvisitor.visit_multiply(self):
            BinaryExpression.accept(self, astvisitor)

    def __repr__(self):
        return "ast.MulOp(%r, %r)" % ((self.lhs), (self.rhs))

class Divide(BinaryExpression):
    """ Divide; /. """

    def accept(self, astvisitor):
        if astvisitor.visit_divide(self):
            BinaryExpression.accept(self, astvisitor)

    def __repr__(self):
        return "ast.DivOp(%r, %r)" % ((self.lhs), (self.rhs))

class Mod(BinaryExpression):
    """ Mod; %. """

    def accept(self, astvisitor):
        if astvisitor.visit_mod(self):
            BinaryExpression.accept(self, astvisitor)

    def __repr__(self):
        return "ast.Mod(%r, %r)" % ((self.lhs), (self.rhs))

# # Unary

class UnaryExpression(Node):
    """ Unary Expression """

    def __init__(self, expression, sourceposition):
        Node.__init__(self, sourceposition)
        self.expression = expression

    def get_expression(self):
        return self.expression

    def accept(self, astvisitor):
        if astvisitor.visit_unaryexpression(self):
            self.expression.accept(astvisitor)

class UnaryNot(UnaryExpression):
    """ Unary Not expression; not [x]; """

    def accept(self, astvisitor):
        if astvisitor.visit_unarynot(self):
            UnaryExpression.accept(self, astvisitor)

    def __repr__(self):
        return "ast.UnaryNot(%r)" % (self.expression)

class UnaryNegate(UnaryExpression):
    """ Unary negate;  - [x] """

    def accept(self, astvisitor):
        if astvisitor.visit_unarynegate(self):
            UnaryExpression.accept(self, astvisitor)

    def __repr__(self):
        return "ast.UnaryNegate(%r)" % (self.expression)

# Flow Control

class WhileStatement(Node):
    """ while [condition] { [block] } """

    def __init__(self, condition, block, sourceposition):
        Node.__init__(self, sourceposition)
        assert isinstance(condition, Node) # RPython

        self.condition = condition
        self.block = block

    def get_condition(self):
        return self.condition

    def get_block(self):
        return self.block

    def accept(self, astvisitor):
        if astvisitor.visit_whilestatement(self):
            self.condition.accept(astvisitor)
            self.block.accept(astvisitor)

    def __repr__(self):
        return "ast.WhileStatement(condition=%r, block=%r)" % (self.condition, self.block)

class BreakStatement(Node):

    def __init__(self, sourceposition):
        Node.__init__(self, sourceposition)

    def accept(self, astvisitor):
        astvisitor.visit_breakstatement(self)

    def __repr__(self):
        return "ast.BreakStatement()"

class ContinueStatement(Node):

    def __init__(self, sourceposition):
        Node.__init__(self, sourceposition)

    def accept(self, astvisitor):
        astvisitor.visit_continuestatement(self)

    def __repr__(self):
        return "ast.ContinueStatement()"

class IfStatement(Node):
    """ if [condition] { [block] } """

    def __init__(self, condition, ifclause, sourceposition):
        Node.__init__(self, sourceposition)
        self.condition = condition
        self.ifclause = ifclause

    def get_condition(self):
        return self.condition

    def get_block(self):
        return self.ifclause

    def accept(self, astvisitor):
        if astvisitor.visit_ifstatement(self):
            self.condition.accept(astvisitor)
            self.ifclause.accept(astvisitor)

    def __repr__(self):
        return "ast.IfStatement(condition=%r, block=%r)" % (self.condition, self.ifclause)

# Built ins

class PrintStatement(Node):
    """ print [statement] """

    def __init__(self, expression, sourceposition):
        Node.__init__(self, sourceposition)
        self.expression = expression

    def get_expression(self):
        return self.expression

    def accept(self, astvisitor):
        if astvisitor.visit_printstatement(self):
            self.expression.accept(astvisitor)

    def __repr__(self):
        return "ast.PrintStatement(%r)" % (self.expression)

# Functions

class ParameterList(Node):
    """ Function definition parameter list: fn ([parameters]) """
    def __init__(self, parameters, sourceposition):
        """ Args:
                parameters -- A list of parameters
        """
        Node.__init__(self, sourceposition)
        self.parameters = parameters

    def get_parameter_list(self):
        return self.parameters

    def accept(self, astvisitor):
        astvisitor.visit_parameterlist(self)

    def __repr__(self):
        return "ast.ParameterList(%r)" % self.parameters

class ArgumentList(Node):
    """ Function call argument list """

    def __init__(self, arglist, sourceposition):
        """ Args:
                arglist -- A List of expressions
        """
        Node.__init__(self, sourceposition, sourceposition)
        self.arguments = arglist

    def get_argument_list(self):
        return self.arguments

    def accept(self, astvisitor):
        if astvisitor.visit_argumentlist(self):
            for arg in self.arguments:
                arg.accept(astvisitor)

    def __repr__(self):
        return "ast.FunctionArgList(%r)" % (self.arguments)

class FunctionExpression(Node):
    """ A function expression:  fn([paramlist]) { [block] } """

    def __init__(self, paramlist, block, sourceposition):
        Node.__init__(self, sourceposition)
        self.paramlist = paramlist
        self.block = block

    def get_parameterlist(self):
        return self.paramlist

    def accept(self, astvisitor):
        if astvisitor.visit_functionexpression(self):
            self.block.accept(astvisitor)

    def __repr__(self):
        return "ast.FunctionExpression(paramlist=%r, block=%r)" % (self.paramlist, self.block)

class FunctionStatement(Node):
    """ A function statement: fn [identifier]([paramlist]) { [block] } """

    def __init__(self, identifier, paramlist, block, sourceposition):
        Node.__init__(self, sourceposition)
        self.identifier = identifier
        self.paramlist = paramlist
        self.block = block

    def get_parameters(self):
        return self.paramlist

    def get_name(self):
        return self.identifier

    def accept(self, astvisitor):
        if astvisitor.visit_functionstatement(self):
            self.block.accept(astvisitor)

    def __repr__(self):
        return "ast.FunctionStatement(%r, %r, %r)" % (self.identifier, self.paramlist, self.block)

class FunctionCall(Node):
    """ Function call: [identifier]([arglist]) """

    def __init__(self, identifier, arglist, sourceposition):
        Node.__init__(self, sourceposition)
        self.identifier = identifier
        self.arglist = arglist

    def get_arguments(self):
        return self.arglist

    def get_identifier(self):
        return self.identifier

    def accept(self, astvisitor):
        if astvisitor.visit_functioncall(self):
            for arg in self.get_arguments():
                arg.accept(astvisitor)

    def __repr__(self):
        return "ast.FunctionCall(%r, %r)" % (self.identifier, self.arglist)

class AsyncFunctionCall(Node):
    """ Function call: [identifier]([arglist]) """

    def __init__(self, identifier, arglist, sourceposition):
        Node.__init__(self, sourceposition)
        self.identifier = identifier
        self.arglist = arglist

    def get_arguments(self):
        return self.arglist

    def get_identifier(self):
        return self.identifier

    def accept(self, astvisitor):
        if astvisitor.visit_asyncfunctioncall(self):
            for arg in self.get_arguments():
                arg.accept(astvisitor)

    def __repr__(self):
        return "ast.AsyncFunctionCall(%r, %r)" % (self.identifier, self.arglist)


class ReturnStatement(Node):
    def __init__(self, expression, sourceposition):
        Node.__init__(self, sourceposition)
        self.expression = expression

    def get_expression(self):
        return self.expression

    def accept(self, astvisitor):
        if astvisitor.visit_returnstatement(self):
            self.expression.accept(astvisitor)

    def __repr__(self):
        return "ast.ReturnStatement(%r)" % (self.expression)

# Value Expressions

class IdentifierExpression(Node):
    """ identifier: 'a' """

    def __init__(self, identifier, sourceposition):
        Node.__init__(self, sourceposition)
        self.identifier = identifier

    def get_identifier(self):
        return self.identifier

    def accept(self, astvisitor):
        astvisitor.visit_identifierexpression(self)

    def __repr__(self):
        return "ast.IdentifierExpression(%r)" % (self.identifier)

class ArrayAccess(Node):
    """ Array access: {identifier}[{index}]; """
    def __init__(self, identifier, index, sourceposition):
        Node.__init__(self, sourceposition)
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
        return "ast.ArrayAccess(identifier=%r, index=%r)" % (self.identifier, self.index)

class ArrayAssignment(Node):

    def __init__(self, array_access, expression, sourceposition):
        Node.__init__(self, sourceposition)
        assert isinstance(array_access, ArrayAccess)  # RPython

        self.array_access = array_access
        self.expression = expression

    def get_array_access(self):
        return self.array_access

    def get_expression(self):
        return self.expression

    def accept(self, astvisitor):
        if astvisitor.visit_arrayassignment(self):
            self.array_access.accept(astvisitor)
            self.expression.accept(astvisitor)

    def __repr__(self):
        return "ast.ArrayAssignment(%r, %r)" % (self.array_access, self.expression)

# Channel Expressions

class ChannelIn(Node):

    def __init__(self, channel_identifier, expression_in, sourceposition):
        Node.__init__(self, sourceposition)
        self.channel = channel_identifier
        self.expression = expression_in

    def get_channel(self):
        return self.channel

    def get_expression(self):
        return self.expression

    def accept(self, astvisitor):
        if astvisitor.visit_channelin(self):
            self.expression.accept(astvisitor)
            self.channel.accept(astvisitor)

    def __repr__(self):
        return "ast.ChannelIn(%r, %r)" % (self.channel, self.expression)

class ChannelOut(Node):

    def __init__(self, channel_identifier, sourceposition):
        Node.__init__(self, sourceposition)
        self.channel = channel_identifier

    def get_channel(self):
        return self.channel

    def accept(self, astvisitor):
        if astvisitor.visit_channelout(self):
            self.channel.accept(astvisitor)

    def __repr__(self):
        return "ast.ChannelOut(%r)" % (self.channel)

class ASTVisitor(object):
    pass

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
        setattr(ASTVisitor, 'visit_' + cls[0].lower(), _visit)

_create_visitor()
