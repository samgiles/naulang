from wlvlang.compiler.ast import Operator, ASTVisitor

class Block(object):

    def __init__(self, previous_block):
        self.tacs = {}
        self.child_blocks = {}
        self.symbol_map = {}

    def get_tacs(self):
        return self.tacs

class TACGen(ASTVisitor):
    """ Generate Three Address Code """

    def __init__(self, space):
        self.symbol_index = 0
        self.root_block = Block(None)
        self.current_block = self.root_block

    def get_current_block(self):
        return self.current_block

    def get_symbol_map(self):
        return self.symbol_map

    def next_label(self):
        value_label = "v" + str(self.symbol_index)
        self.symbol_index += 1
        return value_label

    def last_label(self):
        return "v" + str(self.symbol_index - 1)

    def visit_booleanconstant(self, node):
        label = self.next_label()
        self.current_block.tacs[label] = (Operator.CONST, node.get_boolean_value(), None)
        return True

    def visit_integerconstant(self, node):
        label = self.next_label()
        self.current_block.tacs[label] = (Operator.CONST, node.get_integer_constant(), None)
        return True

    def visit_stringconstant(self, node):
        label = self.next_label()
        self.current_block.tacs[label] = (Operator.CONST, node.get_string_value(), None)
        return True

    def visit_assignment(self, node):
        node.expression.accept(self)
        variable_name = node.get_varname()
        label = self.last_label()
        self.current_block.symbol_map[label] = variable_name
        return False

    def visit_binaryexpression(self, node):
        node.lhs.accept(self)
        left_label = self.last_label()

        node.rhs.accept(self)
        right_label = self.last_label()

        label = self.next_label()
        self.current_block.tacs[label] = (node.get_operator(), left_label, right_label)
        return False

    def visit_unarynot(self, node):
        node.expression.accept(self)
        expression_label = self.last_label()
        self.current_block.tacs[expression_label] = (Operator.NOT, expression_label, None)
        return False

    def visit_unarynegate(self, node):
        node.expression.accept(self)
        expression_label = self.last_label()
        self.current_block.tacs[expression_label] = (Operator.NEGATE, expression_label, None)
        return False

    def visit_breakstatement(self, node):
        pass

    def visit_continuestatement(self, node):
        pass

    def visit_whilestatement(self, node):
        pass

    def visit_ifstatement(self, node):
        pass

    def visit_printstatement(self, node):
        pass

    def visit_identifierexpression(self, node):
        pass

