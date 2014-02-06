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
        return "Block(%r)" % (repr(self._statements))


class Statement(Node):
    def __init__(self, expression):
        self._expression = expression

    def compiler(self, context):
        self._expression.compile(context)

    def __repr__(self):
        return "Statement(%r)" % (repr(self._expression))

class BooleanConstant(Node):

    def __init__(self, value):
        self._value = value

    def compile(self, context):
        from wlvlang.vmobjects.boolean import Boolean
        boolean = Boolean(self._value)
        context.emit(Bytecode.LOAD_CONST, context.register_constant(boolean))

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
        from wlvlang.vmobjects.integer import Integer
        integer = Integer(self._value)
        context.emit(Bytecode.LOAD_CONST, context.register_constant(integer))

    def __repr__(self):
        return "IntegerConstant(%d)" % (self._value)

class Assignment(Node):

    def __init__(self, variable_name, expression):
        self._varname = variable_name
        self._expression = expression

    def compiler(self, context):
        pass

    def __repr__(self):
        return "Assignment(%s, %r)" % (self._varname, repr(self._expression))

class Or(Node):

    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.OR)

    def __repr__(self):
        return "Or(%r, %r)" % (repr(self._lhs), repr(self._rhs))

class And(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.AND)

    def __repr__(self):
        return "And(%r, %r)" % (repr(self._lhs), repr(self._rhs))

class Equals(Node):

    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.EQUAL)

    def __repr__(self):
        return "Equals(%r, %r)" % (repr(self._lhs), repr(self._rhs))

class NotEquals(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.NOT_EQUAL)

    def __repr__(self):
        return "NotEquals(%r, %r)" % (repr(self._lhs), repr(self._rhs))

class LessThan(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.LESS_THAN)

    def __repr__(self):
        return "LessThan(%r, %r)" % (repr(self._lhs), repr(self._rhs))

class LessThanOrEqual(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.LESS_THAN_EQ)
    def __repr__(self):
        return "LessThanOrEqual(%r, %r)" % (repr(self._lhs), repr(self._rhs))

class GreaterThan(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.GREATER_THAN)

    def __repr__(self):
        return "GreaterThan(%r, %r)" % (repr(self._lhs), repr(self._rhs))

class GreaterThanOrEqual(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.LESS_THAN_EQ)
    def __repr__(self):
        return "GreaterThanOrEqual(%r, %r)" % (repr(self._lhs), repr(self._rhs))

class AddOp(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.ADD)

    def __repr__(self):
        return "AddOp(%r, %r)" % (repr(self._lhs), repr(self._rhs))

class SubtractOp(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.SUB)

    def __repr__(self):
        return "SubtractOp(%r, %r)" % (repr(self._lhs), repr(self._rhs))

class MulOp(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.MUL)

    def __repr__(self):
        return "MulOp(%r, %r)" % (repr(self._lhs), repr(self._rhs))

class DivOp(Node):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def compile(self, context):
        self._lhs.compile(context)
        self._rhs.compile(context)
        context.emit(Bytecode.DIV)

    def __repr__(self):
        return "DivOp(%r, %r)" % (repr(self._lhs), repr(self._rhs))

class UnaryNot(Node):
    def __init__(self, expression):
        self._expression = expression

    def compile(self, context):
        self._expression.compile(context)
        context.emit(Bytecode.NOT)

    def __repr__(self):
        return "UnaryNot(%r)" % (repr(self._expression))

class UnaryNegate(Node):
    def __init__(self, expression):
        self._expression = expression

    def compile(self, context):
        self._expression.compile(context)
        context.emit(Bytecode.NEG)

    def __repr__(self):
        return "UnaryNegate(%r)" % (repr(self._expression))

class WhileStatement(Node):

    def __init__(self, condition, block):
        self._condition = condition
        self._statements = block

    def compile(self, context):
        pos = len(context.data)
        self._condition.compile(context)
        context.emit(bytecode.JUMP_IF_FALSE)
        jmp_back_to = len(context.data) - 1
        self._statements.compile(context)
        context.emit(Bytecode.JUMP_BACK, pos)
        context.data[jmp_back_to] = chr(len(context.data))

    def __repr__(self):
        return "WhileStatement(condition=%r, block=%r)" % (repr(self._condition), repr(self._block))

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
        return "IfStatement(condition=%r, block=%r)" % (repr(self._condition), repr(self._block))

class PrintStatement(Node):
    def __init__(self, expression):
        self._expression = expression

    def compile(self, context):
        self._expression.compile(context)
        context.emit(Bytecode.PRINT)

    def __repr__(self):
        return "PrintStatement(%r)" % (repr(self._condition))

class Transformer(object):

    def _get_statements(self, kleene):
        statements = []

        while len(kleene.children) == 2:
            statements.append(self.visit_stmt(kleene.children[0]))
            kleene = kleene.children[1]

        statements.append(self.visit_stmt(kleene.children[0]))
        return statements

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
            return Equals(self.visit_relation(node.children[0]), self.visit_expr(node.children[2]))

        if node.children[1].additional_info == "!=":
            return NotEquals(self.visit_relation(node.children[0]), self.visit_expr(node.children[2]))

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

        raise TypeError("Failed to parse an atom")


    def visit_booleanliteral(self, node):
        if node.additional_info == "true":
            return BooleanConstant(True)

        return BooleanConstant(False)

    def visit_numericliteral(self, node):
        if node.symbol == "FLOATLITERAL":
            pass # TODO

        if node.symbol == "INTEGERLITERAL":
            # TODO: Convert string to bigint accordingly
            return IntegerConstant(int(node.additional_info))

    def visit_stringliteral(self, node):
        return StringConstant(node.children[0].additional_info)

    def visit_stmt(self, node):

        if len(node.children) == 3 and node.children[1].additional_info == "=":
            # Normal assignment
            return Assignment(node.children[0].symbol, self.visit_bool(node.children[2]))

        if node.children[0].additional_info == 'while':
            return WhileStatement(self.visit_bool(node.children[2]), self._get_statements(node.children[5]))

        if node.children[0].additional_info == 'if':
            return IfStatement(self.visit_bool(node.children[2]), self._get_statements(node.children[5]))

        if node.children[0].additional_info == 'print':
            return PrintStatement(self.visit_bool(node.children[1]))

