class VM_Exception(Exception):
    pass

class MethodNotFoundException(VM_Exception):

    def __init__(self, signature, classs):
        self.classs = classs
        self.signature = signature
