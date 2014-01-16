
class Node:
    pass

class LetEq(Node):
    """ Defines a node for the 'let [symbol] = [expression]' sub expression"""

    def __init__(self, value_expression, identifier):
        self.value_expression = value_expression
        self.symbol = identifier

    def child_value_expression(self):
        return self.value_expression

    def child_symbol(self):
        return self.symbol

class WhileExpression(Node):

    def __init__(self, conditionexpression, bodystatements):
        self.condition_expr = conditionexpression
        self.bodystatements = bodystatements

    def child_condition_expr(self):
        return self.condition_expr

    def child_bodystatements(self):
        return self.bodystatements

class IfExpression(Node):

    def __init__(self, conditionexpression, truestatements, falsestatements):
        self.condition_expr = conditionexpression
        self.truestatement = truestatements
        self.falsestatement = falsestatements

    def child_condition_expr(self):
        return self.condition_expr

    def child_truestatements(self):
        return self.truestatement

    def child_falsestatements(self):
        return self.falsestatement
