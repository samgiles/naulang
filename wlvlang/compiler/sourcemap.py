"""
    Maps a bytecode list for a method to line numbers and column numbers.
"""

class SourceMap(object):

    def __init__(self):
        self.source_to_bytecode_map = {}

    def add(self, pc, sourceposition):
        self.source_to_bytecode_map[pc] = sourceposition

    def get(self, pc):
        return self.source_to_bytecode_map[pc]
