class CompilerException(Exception):

    def __init__(self, message, sourcepos):
        Exception.__init__(self, message)
        self.sourcepos = sourcepos

    def getsourcepos(self):
        return self.sourcepos
