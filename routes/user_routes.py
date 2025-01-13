from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from config.database import get_db
from schemas import user_schema
from utilities.error_handler import UnicornException
from controllers import user_controllers
from middleware.auth_middleware import auth

router = APIRouter()


@router.post('/register')
def register_user( payload: user_schema.User, db: Session = Depends(get_db)):
    try:
       return user_controllers.register_user(payload, db)
    except Exception as err:
        raise UnicornException(str(err))
@router.post('/log-in')
def log_in( payload: user_schema.Login, db: Session = Depends(get_db)):
    try:
       return user_controllers.log_in(payload, db)
    except Exception as err:
        raise err
    
@router.get('/me')
def me(request: Request, current_user = Depends(auth)):
    try:
       return user_controllers.me(request)
    except Exception as err:
        raise err