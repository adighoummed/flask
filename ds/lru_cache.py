# from ds.doubly_linked_list import DoublyLinkedList, Node
from typing import Optional, List, Dict

from ds.queue import Queue, Node


class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.queue = Queue()
        self.map: Dict[str, Node] = {}

    def get(self, key: str) -> List[str]:
        if key in self.map:
            node = self.map[key]
            self.queue.move_to_head(node)
            return node.get_data()
        else:
            return []

    def put(self, key: str, value: List[str]) -> None:
        if key not in self.map:
            if self.queue.get_size() == self.capacity:
                head = self.queue.dequeue_from_last()
                del self.map[head.key]
            # node = Node(key, value)
            new_node = self.queue.enqueue_at_first(key, value)
            self.map[key] = new_node
