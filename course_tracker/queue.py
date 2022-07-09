import typing

# Basic implementation of a queue to be used to handle incoming requests from the bot commands.
class Queue:
    class _Node:
        def __init__(self, val: typing.Any) -> None:
            self.next = None
            self.prev = None
            self.val = val

    def __init__(self) -> None:
        self._header = self._Node(None)
        self._trailer = self._Node(None)
        self._size = 0

        self._header.next = self._trailer
        self._trailer.prev = self._header

    # Returns the length of the queue not including the header and trailer
    def __len__(self) -> None: 
        return self._size

    # Add a node to the front of the queue
    def enqueue(self, value: typing.Any) -> None:
        node = self._Node(value)

        self._header.next.prev = node
        node.next = self._header.next
        self._header.next = node
        node.prev = self._header

        self._size += 1

    # Remove a node from the end of the queue
    def dequeue(self) -> typing.Any:
        if self.size == 0:
            raise Empty

        node = self._trailer.prev
        self._trailer.prev = self._trailer.prev.prev
        self._trailer.prev.next = self._trailer

        self._size -= 1

        return node.val

# Custom exception for when a queue is empty
class Empty(Exception):
    pass