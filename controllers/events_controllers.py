from schemas.event_schema import EventCreate
from models.event_modal import Event, EventStatus
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import and_


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
    
def get_all_events(db: Session, status: str = None, location: str = None, start_date: datetime = None, end_date: datetime = None,   page: int = 1, page_size: int = 10,):
    try:
        query = db.query(Event)
        
        if status:
            query = query.filter(Event.status == status)
        if location:
            query = query.filter(Event.location.ilike(f"%{location}%"))
        if start_date:
            query = query.filter(Event.start_time >= start_date)
        if end_date:
            query = query.filter(Event.end_time <= end_date)

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        events = query.all()

        total_count = db.query(Event).filter(
            and_(
                (Event.status == status if status else True),
                (Event.location.ilike(f"%{location}%") if location else True),
                (Event.start_time >= start_date if start_date else True),
                (Event.end_time <= end_date if end_date else True)
            )
        ).count()
        
        return {
            "success": True,
            "data": events if events else [],
            "total_count": total_count,
            "page": page,
            "page_size": page_size,
            "total_pages": (total_count + page_size - 1) // page_size  
        }
    except Exception as e:
        raise UnicornException(str(e))

