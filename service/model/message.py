from sqlalchemy.orm import declarative_base
from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy.sql import func

Base = declarative_base()


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    sensor_name = Column(String(40))
    value = Column(Integer)
