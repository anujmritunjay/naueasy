import datetime
from typing import Optional
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
    

@router.get('/get-events')  
def get_events(
    status: Optional[str] = None,
    location: Optional[str] = None,
    start_date: Optional[datetime.datetime] = None,
    end_date: Optional[datetime.datetime] = None,
    page: int = 1,
    page_size: int = 10,
    current_user = Depends(auth),  # Optional: Include authentication if needed
    db: Session = Depends(get_db)
):
    try:
        # Fetch events using the controller function, which includes filters and pagination
        result = events_controllers.get_all_events(
            db=db,
            status=status,
            location=location,
            start_date=start_date,
            end_date=end_date,
            page=page,
            page_size=page_size
        )
        return result
    except Exception as err:
        raise UnicornException(str(err))
