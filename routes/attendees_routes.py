from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from schemas import attendees_schema
from utilities.error_handler import UnicornException
from controllers import attendees_controllers
from middleware.auth_middleware import auth

router = APIRouter()


@router.post('/register-attendees')
def create_event( payload: attendees_schema.AttendeeRegister, current_user = Depends(auth), db: Session = Depends(get_db)):
    try:
       return attendees_controllers.attendee_register(payload, db)
    except Exception as err:
        raise UnicornException(str(err))
    
@router.put('/check-in-status')
def update_event(attendee_id: int, payload: attendees_schema.UpdateCheckInStatus, current_user = Depends(auth), db: Session = Depends(get_db)):
    try:
       return attendees_controllers.check_in_status(attendee_id, payload, db)
    except Exception as err:
        raise UnicornException(str(err))