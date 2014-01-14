
class Node:
    pass

class LetEq(Node):
    """ Defines a node for the 'let [symbol] = [expression]' sub expression"""

    def __init__(self, value_expression, identifier):
        self.child_value_expression = value_expression
        self.child_symbol = identifier

    def child_value_expression(self):
        return self.child_value_expression

    def child_symbol(self):
        return self.child_symbol
