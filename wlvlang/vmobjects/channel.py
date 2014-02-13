from wlvlang.vmobjects.object import Object

class Channel(Object):

    def __init__(self):
        self.queue = []

    def get_class(self, universe):
        pass

    def __repr__(self):
        return "wlvlang.Channel()"
