from ds.doubly_linked_list import DoublyLinkedList, Node


class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.queue = DoublyLinkedList()
        self.map = {}

    def get(self, key: int) -> int:
        if key in self.map:
            node = self.map[key]
            self.queue.remove(node)
            self.queue.add_to_tail(node)
            return node.value
        else:
            return -1

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            self.queue.remove(self.map[key])
        elif self.queue.size() == self.capacity:
            head = self.queue.remove_from_head()
            del self.map[head.key]
        node = Node(key, value)
        self.queue.add_to_tail(node)
        self.map[key] = node

