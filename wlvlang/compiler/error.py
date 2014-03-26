class CompilerException(Exception):

    def __init__(self, message, sourcepos):
        self.message = message
        self.sourcepos = sourcepos

    def getsourcepos(self):
        return self.sourcepos
