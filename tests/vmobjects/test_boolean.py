import pytest

from wlvlang.vmobjects.boolean import Boolean

def test_get_value():
    subjecta = Integer(True)
    subjectb = Integer(False)

    assert(subjecta.get_value() == True)
    assert(subjectb.get_value() == False)
