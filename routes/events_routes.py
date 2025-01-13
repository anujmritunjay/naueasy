from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from config.database import get_db
from schemas import event_schema
from utilities.error_handler import UnicornException
from controllers import events_controllers
from middleware.auth_middleware import auth

router = APIRouter()


@router.post('/add-event')
def create_event( payload: event_schema.EventCreate, current_user = Depends(auth), db: Session = Depends(get_db)):
    try:
       return events_controllers.create_event(payload, db)
    except Exception as err:
        raise UnicornException(str(err))
    
@router.put('/update-event')
def update_event(event_id: int, payload: event_schema.EventCreate, current_user = Depends(auth), db: Session = Depends(get_db)):
    try:
       return events_controllers.update_event(event_id, payload, db)
    except Exception as err:
        raise UnicornException(str(err))