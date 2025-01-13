from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class EventStatus(str, Enum):
    SCHEDULED = "scheduled"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELED = "canceled"

class EventBase(BaseModel):
    name: str = Field(..., max_length=255, description="Name of the event")
    description: str | None = Field(None, max_length=1000, description="Description of the event")
    start_time: datetime = Field(..., description="Event start time")
    end_time: datetime = Field(..., description="Event end time")
    location: str | None = Field(None, max_length=255, description="Event location")
    max_attendees: int = Field(..., ge=0, description="Maximum number of attendees")
    status: EventStatus = Field(EventStatus.SCHEDULED, description="Current status of the event")

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    pass
