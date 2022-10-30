import threading

from service.repository.repository import Repository
from utils.network import Network


class Logger(threading.Thread):
    def __init__(self, repository: Repository, network: Network, id: int):
        super().__init__()
        self.repository: Repository = repository
        self.network: Network = network
        self.id = id

    def run(self) -> None:
        print(f"Starting consumer: {self.id}")
        try:
            while True:
                message = self.network.consume()
                if message is None:
                    self.network.publish(None)
                    break
                print(f"Consumer {self.id} got message: {message}")
                self.repository.save(message)
            print(f"Stopping consumer {self.id}")
        finally:
            print(f"Stopped consumer {self.id}")
