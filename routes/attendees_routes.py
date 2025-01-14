from fastapi import APIRouter, Depends, File, UploadFile
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

@router.get('/get-attendees/{event_id}')
def get_attendees(event_id: str, page: int = 1, limit: int = 10, current_user = Depends(auth), db: Session = Depends(get_db)):
    try:
        return attendees_controllers.get_attendees(event_id, db, page, limit)
    except Exception as err:
        raise UnicornException(str(err))

@router.post('/bulk-checkin')
async def bulk_checkin(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        result = attendees_controllers.bulk_checkin(file, db)
        return result
    except UnicornException as e:
        raise UnicornException(str(e))

