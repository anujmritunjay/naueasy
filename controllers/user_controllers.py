from models.user_model import User
from schemas.user_schema import User as u_schema
from sqlalchemy.orm import Session
from services import user_services
from sqlalchemy import or_



def register_user(payload:u_schema , db: Session):
    try:
        is_exists = db.query(User).filter(or_(User.email == payload.email, User.username == payload.username)).first()
        if is_exists:
            raise Exception('User already exists.')
        hash_pass = user_services.hash_password(payload.password)
        print(hash_pass)
        user = User(username=payload.username, password=hash_pass, email=payload.email)        
        db.add(user)
        db.commit()
        db.refresh(user)
        return {
            "success": True,
            "data": user
        }
    except Exception as e:
        raise e