import typing

class Queue:
    """Basic implementation of a queue to be used to handle incoming requests from the bot commands."""

    class _Node:
        """Represents an individual element of the Queue."""

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

    def __len__(self) -> None:
        """Return the length of the queue."""

        return self._size

    def enqueue(self, value: typing.Any) -> None:
        """Add an item to the front of the queue.
        
        Args:
            value: The item to be added to the queue.
        """

        node = self._Node(value)

        self._header.next.prev = node
        node.next = self._header.next
        self._header.next = node
        node.prev = self._header

        self._size += 1

    def dequeue(self) -> typing.Any:
        """Remove an item from the end of the queue.
        
        Returns:
            The item that was removed.
        """
        if self._size == 0:
            raise Empty

        node = self._trailer.prev
        self._trailer.prev = self._trailer.prev.prev
        self._trailer.prev.next = self._trailer

        self._size -= 1

        return node.val

class Empty(Exception):
    """Custom exception representing when a queue is empty."""
    pass