

class ActivationRecord(object):

    def __init__(self, previous_record):
        self.previous_record = previous_record

    def get_previous_record(self):
        return self.previous_record

    def is_root_record(self):
        return self.get_previous_record() == None
