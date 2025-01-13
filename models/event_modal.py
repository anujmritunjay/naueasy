from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum
from config.database import Base


# Define the status enumeration
class EventStatus(PyEnum):
    SCHEDULED = "scheduled"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELED = "canceled"

# Event model
class Event(Base):
    __tablename__ = "events_tbl"

    event_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=True)
    max_attendees = Column(Integer, nullable=False, default=0)
    status = Column(Enum(EventStatus), nullable=False, default=EventStatus.SCHEDULED)

