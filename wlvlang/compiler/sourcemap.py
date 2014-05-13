class SourceMap(object):
    """
        Maps a sequence of bytecodes for a method to
        line numbers and column numbers.
    """

    def __init__(self):
        self.source_to_bytecode_map = {}

    def add(self, pc, sourceposition):
        self.source_to_bytecode_map[pc] = sourceposition

    def get(self, pc):
        try:
            return self.source_to_bytecode_map[pc]
        except:
            return None
