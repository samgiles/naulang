import pytest

from wlvlang.vmobjects.symbol import Symbol

def test_get_arguments_as_list():
    subject = Symbol("list.reverse.map")

    print(repr(subject._arguments))
    assert(subject._argument_count == 3)
    assert(subject._arguments == ["list", "reverse", "map"])
