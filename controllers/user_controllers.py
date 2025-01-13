from models.user_model import User
from schemas.user_schema import User as u_schema, Login
from sqlalchemy.orm import Session
from services import user_services
from sqlalchemy import or_

from utilities.error_handler import UnicornException



def register_user(payload:u_schema , db: Session):
    try:
        is_exists = db.query(User).filter(User.email == payload.email).first()
        if is_exists:
            raise Exception('User already exists.')
        hash_pass = user_services.hash_password(payload.password)
        print(hash_pass)
        user = User(name=payload.username, password=hash_pass, email=payload.email)        
        db.add(user)
        db.commit()
        db.refresh(user)
        return {
            "success": True,
            "data": user
        }
    except Exception as e:
        raise e
    
def log_in(payload:Login , db: Session):
    try:
        user = db.query(User).filter(User.email == payload.email).first()
        if not user:
            raise UnicornException("Invalid Credentials.", 401)

        is_pass_match = user_services.compare_password(payload.password, user.password)
        
        if not is_pass_match:
            raise UnicornException("Invalid Credentials.", 401)

        token = user_services.generate_jwt({"id": user.id})
        del user.password
        return {
            "success": True,
            "data": user,
            "token": token
        }
        
    except Exception as err:
        raise UnicornException(str(err))