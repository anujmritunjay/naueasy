from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from config.database import Base


class Attendee(Base):
    __tablename__ = 'attendees'

    attendee_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
    event_id = Column(Integer, ForeignKey('events_tbl.event_id'), nullable=False)
    check_in_status = Column(Boolean, default=False)

  