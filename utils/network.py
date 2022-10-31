import queue
from service.model.message import Message


class Network:
    def __init__(self, buffer: queue.Queue):
        self._buffer = buffer

    def publish(self, message: Message) -> None:
        self._buffer.put(message)

    def consume(self):
        return self._buffer.get()
