from schemas.event_schema import EventCreate
from models.event_modal import Event, EventStatus
from sqlalchemy.orm import Session
from datetime import datetime

from utilities.error_handler import UnicornException



def create_event(payload:EventCreate , db: Session):
    try:
        new_event = Event(
        name=payload.name,
        description=payload.description,
        start_time=payload.start_time,
        end_time=payload.end_time,
        location=payload.location,
        max_attendees=payload.max_attendees,
        status=EventStatus.SCHEDULED,
        )
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        return {
            "success": True,
            "data": new_event
        }
    except Exception as e:
        raise UnicornException(str(e))
    
def update_event(event_id, payload: EventCreate, db: Session):
    try:
        event = db.query(Event).filter(Event.event_id == event_id).first()
        
        if not event:
            raise UnicornException(f"Event with ID {event_id} not found.")

        # Update the event details
        event.name = payload.name
        event.description = payload.description
        event.start_time = payload.start_time
        event.end_time = payload.end_time
        event.location = payload.location
        event.max_attendees = payload.max_attendees
        event.status = payload.status

        # Commit the changes
        db.commit()
        db.refresh(event)
        
        return {
            "success": True,
            "data": event
        }
    except Exception as e:
        raise UnicornException(str(e))
