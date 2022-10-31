import threading
import logging

from service.repository.repository import Repository
from utils.network import Network


class Logger(threading.Thread):
    def __init__(self, repository: Repository, network: Network, id: int):
        super().__init__()
        self.repository: Repository = repository
        self.network: Network = network
        self.id = id

    def run(self) -> None:
        try:
            while True:
                message = self.network.consume()
                if message is None:
                    self.network.publish(None)
                    break
                logging.info(f"Consumer {self.id} got message: {message}")
                self.repository.save(message)
            logging.debug(f"Stopping consumer {self.id}")
        finally:
            logging.debug(f"Stopped consumer {self.id}")
