from wlvlang.compiler.ast import Operator, ASTVisitor

class Block(object):

    def __init__(self, previous_blocks, next_block=None):
        """ Represents a Graph node with one input and at least one output. """
        self.tacs = {}
        self.symbol_map = {}
        self.previous_blocks = previous_blocks
        self.next_block = next_block

    def get_tacs(self):
        return self.tacs

class BooleanBlock(Block):
    def __init__(self, previous_blocks, true_block=None, false_block=None):
        Block.__init__(self, previous_blocks, true_block)
        self.true_block = true_block
        self.false_block = false_block

class SSAGen(ASTVisitor):
    """ Generate Three Address Code """

    def __init__(self, space):
        self.symbol_index = 0
        self.root_block = Block(None)
        self.current_block = self.root_block
        self._loop_controls = []

    def get_root_block(self):
        return self.root_block

    def get_current_block(self):
        return self.current_block

    def set_current_block(self, block):
        self.current_block = block

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
        current_block = self.get_current_block()
        break_block = Block([current_block])
        controls = self._loop_controls[len(self._loop_controls) - 1]
        break_block.next_block = controls[1]
        current_block.next_block = break_block
        self.set_current_block(Block([break_block]))
        return False

    def visit_continuestatement(self, node):
        current_block = self.get_current_block()
        continue_block = Block([current_block])
        controls = self._loop_controls[len(self._loop_controls) - 1]
        continue_block.next_block = controls[0]
        current_block.next_block = continue_block
        self.set_current_block(Block([continue_block]))
        return False

    def visit_whilestatement(self, node):
        current_block = self.get_current_block()

        condition_block = BooleanBlock([current_block], None, None)
        current_block.next_block = condition_block

        loop_block = Block([condition_block], condition_block)
        condition_block.true_block = loop_block
        out_block = Block([condition_block])
        condition_block.false_block = out_block

        self.set_current_block(condition_block)
        node.condition.accept(self)

        self._loop_controls.append((condition_block, out_block))
        self.set_current_block(loop_block)
        node.block.accept(self)
        self._loop_controls.pop()

        self.set_current_block(out_block)
        return False

    def visit_ifstatement(self, node):
        current_block = self.get_current_block()
        condition_block = BooleanBlock([current_block], None, None)
        current_block.next_block = condition_block

        ifstatement_body = Block([condition_block])
        condition_block.true_block = ifstatement_body
        self.set_current_block(condition_block)
        node.condition.accept(self)

        self.set_current_block(ifstatement_body)
        node.ifclause.accept(self)

        out_block = Block([condition_block, ifstatement_body])
        condition_block.false_block = out_block
        self.set_current_block(out_block)


    def visit_printstatement(self, node):
        node.expression.accept(self)
        expression_label = self.last_label()
        self.current_block.tacs[expression_label] = (Operator.PRINT, expression_label, None)

    def visit_functionexpression(self, node):
        pass

    def visit_identifierexpression(self, node):
        pass

class GraphTranslator(object):


    def __init__(self, space):
        self.space = space
        self.current_context = FunctionCompilerContext(space)

    def compile(self, node):
        tacs = node.get_tacs()

        for tac in tacs:

            self.compile_tac(tacs[tac])

            if tac in node.symbol_map:
                # Assign expression
                pass

    def compile_tac(self, tac):
        operator = tac[0]
        arg_1 = tac[1]
        arg_2 = tac[2]


