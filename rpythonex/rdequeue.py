from rpython.rlib import rthread


class Node(object):
    def __init__(self, value):
        self.value = value
        self.prev_link = None
        self.next_link = None

    def __eq__(self, other):
        return self.value is other.value and self.prev_link is other.prev_link and self.next_link is other.next_link

class Dequeue(object):
    def __init__(self):
        self._head_lock = rthread.allocate_lock()
        self._tail_lock = rthread.allocate_lock()
        self.head = None
        self.tail = None

    def create_node(self, value):
        node = Node(value)
        return node

    def push_bottom(self, node):
        with self._tail_lock:
            if self.tail is None:
                self.tail = node
                self.prev_link = self.head
                return

            node.prev_link = self.tail
            self.tail.next_link = node
            self.tail = node

    def push_top(self, node):
        with self._head_lock:
            if self.head is None:
                self.head = node
                self.next_link = self.tail
                return

            node.next_link = self.head
            self.head.prev_link = node
            self.head = node

    def pop_top(self):
        with self._head_lock:
            node = self.head

            if node is None:
                return None

            self.head = node.next_link

        return node

    def pop_bottom(self):
        with self._tail_lock:
            node = self.tail
            if node is None:
                return None

            self.tail = node.prev_link

        return node
