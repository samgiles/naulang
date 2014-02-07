import pytest
from wlvlang.interpreter.activationrecord import ActivationRecord


def test_is_root_record():
    subject = ActivationRecord([], 0, 0, 0, None)

    assert(True == subject.is_root_record())

