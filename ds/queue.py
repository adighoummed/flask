from typing import List, Optional


class Node:
    def __init__(self, data: List[str]) -> None:
        self.data = data
        self.next = None
        self.prev = None

    def get_data(self) -> List[str]:
        return self.data


class Queue:
    def __init__(self) -> None:
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue_at_first(self, data: List[str]) -> None:
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    def dequeue_from_last(self) -> Optional[List[str]]:
        if self.tail is None:
            return None
        else:
            data = self.tail.data
            if self.head == self.tail:
                self.head = None
                self.tail = None
            else:
                self.tail = self.tail.prev
                self.tail.next = None
            self.size -= 1
            return data

    def move_to_head(self, node: Node) -> None:
        if self.head == node:
            return
        if self.tail == node:
            self.dequeue_from_last()
            self.enqueue_at_first(node.data)
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            self.enqueue_at_first(node.data)

    def get_size(self) -> int:
        return self.size
