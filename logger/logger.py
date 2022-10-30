import threading

from service.repository.repository import Repository
from utils.network import Network


class Logger(threading.Thread):
    def __init__(self, repository: Repository, network: Network, id: int):
        self.repository: Repository = repository
        self.network: Network = network
        self.id = id

    def run(self) -> None:
        print(f"Starting consumer: {self.id}")
        while True:
            message = self.network.consume()
            print(f"Consumer {self.id} got message: {message}")
            # self.repository.save()