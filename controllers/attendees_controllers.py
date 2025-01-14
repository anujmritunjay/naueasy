from schemas.attendees_schema import AttendeeRegister, UpdateCheckInStatus
from models.attendees_model import Attendee
from models.event_modal import Event
from sqlalchemy.orm import Session

from utilities.error_handler import UnicornException



def attendee_register(payload:AttendeeRegister , db: Session):
    try:
        event = db.query(Event).filter(Event.event_id == payload.event_id).first()
        if not event:
            raise UnicornException("Event not found.")
        attendees = event.attendees
        if (attendees and len(attendees)) >= event.max_attendees:
            raise UnicornException("No seats available for the booking.")

        new_attendee = Attendee(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        phone_number=payload.phone_number,
        event_id=payload.event_id
    )
        db.add(new_attendee)
        db.commit()
        db.refresh(new_attendee)
        return {
            "success": True,
            "data": new_attendee
        }
    except Exception as e:
        raise e
    
def check_in_status(attendee_id, payload: UpdateCheckInStatus, db: Session):
    try:
        attendee = db.query(Attendee).filter(Attendee.attendee_id == attendee_id).first()
        
        if not attendee:
            raise UnicornException(f"Attendee with ID {attendee_id} not found.")
        attendee.check_in_status = payload.status
       
        db.commit()
        db.refresh(attendee)
        
        return {
            "success": True,
            "data": attendee
        }
    except Exception as e:
        raise UnicornException(str(e))
    
def check_in_status(attendee_id, payload: UpdateCheckInStatus, db: Session):
    try:
        attendee = db.query(Attendee).filter(Attendee.attendee_id == attendee_id).first()
        
        if not attendee:
            raise UnicornException(f"Attendee with ID {attendee_id} not found.")
        attendee.check_in_status = payload.status
       
        db.commit()
        db.refresh(attendee)
        
        return {
            "success": True,
            "data": attendee
        }
    except Exception as e:
        raise UnicornException(str(e))
    

    
def get_attendees(event_id, db: Session, page: int = 1, limit: int = 10):
    try:
        if not event_id:
            raise UnicornException(f"Please provide event id.")

        offset = (page - 1) * limit

        attendees = db.query(Attendee).filter(Attendee.event_id == event_id).offset(offset).limit(limit).all()

        total_count = db.query(Attendee).filter(Attendee.event_id == event_id).count()

        res = [a.__dict__ for a in attendees]

        for attendee in res:
            attendee.pop('_sa_instance_state', None)

        return {
            "success": True,
            "data": res,
            "page": page,
            "total_count": total_count,
        
        }
    except Exception as e:
        raise UnicornException(str(e))

