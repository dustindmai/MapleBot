from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Interval,
    String,
    Time,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Event(Base):
    __tablename__ = "events"
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    event_name = Column(String, unique=True, nullable=False)
    reset_time = Column(Time, nullable=False)
    reset_type = Column(String, nullable=False)
    reset_interval = Column(Interval, nullable=True)
    reset_day = Column(Integer, nullable=True)


class Remindees(Base):
    __tablename__ = "remindees"
    discord_id = Column(BigInteger, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.event_id", ondelete='CASCADE'), primary_key=True)
    server_id = Column(BigInteger, nullable=True)
    is_role = Column(Boolean)
    is_dm = Column(Boolean)
