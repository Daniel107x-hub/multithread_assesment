import queue
from service.model.message import Message


class Network(object):
    _instance = None
    _buffer = None

    def __new__(cls, buffer: queue.Queue):
        if cls._instance is None:
            cls._instance = super(Network, cls).__new__(cls)
            cls._buffer = buffer
        return cls._instance

    def publish(self, message: Message) -> None:
        self._buffer.put(message)

    def consume(self):
        return self._buffer.get()
