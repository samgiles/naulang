import pytest
from wlvlang.interpreter.activationrecord import ActivationRecord

def test_get_previous_record():
    subject = ActivationRecord(0, ActivationRecord(0, None))

    assert(isinstance(subject.get_previous_record(), ActivationRecord))

def test_is_root_record():
    subject = ActivationRecord(0, None)

    assert(True == subject.is_root_record())

