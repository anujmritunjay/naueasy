from fastapi import File, UploadFile
from schemas.attendees_schema import AttendeeRegister, UpdateCheckInStatus
from models.attendees_model import Attendee
from models.event_modal import Event
from sqlalchemy.orm import Session

import csv
from io import StringIO
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



def bulk_checkin(file, db: Session):
    try:
        contents = file.file.read()
        csv_file = StringIO(contents.decode("utf-8"))
        reader = csv.DictReader(csv_file)

        updated_attendees = []
        errors = []

        for row in reader:
            email = row.get('email')
            check_in_status = row.get('check_in_status')

            if not email or check_in_status not in ['True', 'False']:
                errors.append(f"Invalid data in row: {row}")
                continue

            attendee = db.query(Attendee).filter(Attendee.email == email).first()

            if attendee:
                attendee.check_in_status = check_in_status == 'True'
                db.commit()
                updated_attendees.append({
                    "attendee_id": attendee.attendee_id,
                    "email": attendee.email,
                    "check_in_status": attendee.check_in_status
                })
            else:
                errors.append(f"Attendee with email {email} not found.")

        if errors:
            raise UnicornException("\n".join(errors))
        
        # Return a serializable response
        return {"success": True, "message": "All check-in completed", "updated_attendees": updated_attendees}
    except Exception as e:
        raise UnicornException(str(e))
