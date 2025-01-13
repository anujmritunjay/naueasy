from utilities.error_handler import UnicornException
from fastapi import Depends, Request
from utilities import bearer
from config.database import get_db
from sqlalchemy.orm import Session
from services import user_services
from models.user_model import User

token = bearer.HTTPBearer()

def auth(request: Request, token: str = Depends(token),  db: Session = Depends(get_db)):
    try:
        if token and token.credentials:
          token_data = user_services.decode_jwt(token.credentials)
          user = db.query(User).filter(User.id == token_data.get('id')).first()
          if not user:
              raise UnicornException("Unauthorized.", 401)
          request.state.user = user
          return user
        else:
            raise UnicornException("Unauthorized.", 401)
    
    except Exception as e:
        raise UnicornException(str(e))