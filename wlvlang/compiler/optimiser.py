from wlvlang.compiler import ast

class ConstantFolding(ast.ASTVisitor):

    def visit_addop(self, node):

        if isinstance(node._lhs, ast.IntegerConstant) and isinstance(node._rhs, ast.IntegerConstant):
            folded_value = node._lhs._value + node._rhs._value
            return ast.IntegerConstant(folded_value)

        return node
