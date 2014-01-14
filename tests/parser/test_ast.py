import pytest
from wlvlang.compiler.ast import Node, LetEq


def test_leteq():
    subject = LetEq(Node(), "x");

    assert(isinstance(subject.child_value_expression, Node))
    assert(subject.child_symbol == "x")
