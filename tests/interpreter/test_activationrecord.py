import pytest
from wlvlang.interpreter.activationrecord import ActivationRecord

def test_get_previous_record():
    subject = ActivationRecord(ActivationRecord(None))

    assert(isinstance(subject.get_previous_record(), ActivationRecord))

def test_is_root_record():
    subject = ActivationRecord(None)

    assert(True == subject.is_root_record())

