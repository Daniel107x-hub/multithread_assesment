from config import configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

SQLITE_DB = "database.db"


class DatabaseService(object):
    db_engine = None
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
            db_config = configuration.get("db")
            dialect = db_config.get("dialect")
            driver = db_config.get("driver", "")
            host = db_config.get("host")
            port = db_config.get("port")
            username = db_config.get("username")
            password = db_config.get("password")
            name = db_config.get("name", "")
            pool_size = db_config.get("pool_size", 5)
            uri = f"{dialect}{'+' if driver else ''}{driver}"
            if dialect == "sqlite":
                uri = f"{uri}:///{SQLITE_DB}"
                cls.db_engine = create_engine(uri)
            else:
                uri = f"{uri}://" f"{username}:{password}@" f"{host}:{port}/" f"{name}"
                cls.db_engine = create_engine(uri, pool_size=pool_size)
            cls.Session = sessionmaker(bind=cls.db_engine)
        return cls._instance

    @contextmanager
    def scoped_session(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def save(self, obj: object) -> None:
        with self.scoped_session() as session:
            session.add(obj)
