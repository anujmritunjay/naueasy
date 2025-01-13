from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from schemas import user_schema
from utilities.error_handler import UnicornException
from controllers import user_controllers

router = APIRouter()


@router.post('/register')
def register_user( payload: user_schema.User, db: Session = Depends(get_db),):
    try:
       return user_controllers.register_user(payload, db)
    except Exception as err:
        raise UnicornException(str(err))