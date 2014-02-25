class SymbolTable(object):

    def __init__(self):
        self._map = {}

    def lookup(self, string):
        return self._map.get(string, None)

    def insert(self, symbol):
        self._map[symbol.get_string()] = symbol
