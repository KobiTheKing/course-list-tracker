import typing

# Basic implementation of a queue to be used to handle incoming requests from the bot commands.
class Queue:
    class _Node:
        def __init__(self, val: typing.Any) -> None:
            self.next = None
            self.prev = None
            self.val = val

    def __init__(self) -> None:
        self.header = self._Node(None)
        self.trailer = self._Node(None)

        self.header.next = self.trailer
        self.trailer.prev = self.header

    # Add a node to the front of the queue
    def enqueue(self, value: typing.Any) -> None:
        node = self._Node(value)

        self.header.next.prev = node
        node.next = self.header.next
        self.header.next = node
        node.prev = self.header

    # Remove a node from the end of the queue
    def dequeue(self) -> typing.Any:
        if self.header.next == self.trailer:
            raise Empty

        node = self.trailer.prev
        self.trailer.prev = self.trailer.prev.prev
        self.trailer.prev.next = self.trailer

        return node.val

# Custom exception for when a queue is empty
class Empty(Exception):
    pass