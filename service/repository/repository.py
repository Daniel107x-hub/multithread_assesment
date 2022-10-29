from service.database_service import DatabaseService
from service.model.message import Message


class Repository:
    def __init__(self, db: DatabaseService) -> None:
        self._db = db

    def create_tables(self):
        Message.metadata.create_all(self._db.db_engine, checkfirst=True)

    def save(self, message: Message) -> None:
        self._db.save(message)


