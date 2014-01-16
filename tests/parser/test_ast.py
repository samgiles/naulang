import pytest
from wlvlang.compiler.ast import Node, LetEq, WhileExpression, IfExpression


def test_leteq():
    subject = LetEq(Node(), "x");

    assert(isinstance(subject.child_value_expression(), Node))
    assert(subject.child_symbol() == "x")

def test_whilexpression():
    subject = WhileExpression(Node(), [Node(), Node()])

    assert(isinstance(subject.child_condition_expr(), Node))
    assert(isinstance(subject.child_bodystatements(), list))
    assert(isinstance(subject.child_bodystatements()[0], Node))
    assert(isinstance(subject.child_bodystatements()[1], Node))

def test_ifexpression():
    subject = IfExpression(Node(), [Node()], [Node()])

    assert(isinstance(subject.child_condition_expr(), Node))
    assert(isinstance(subject.child_truestatements(), list))
    assert(isinstance(subject.child_falsestatements(), list))
