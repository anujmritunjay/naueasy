from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str  
    email: EmailStr  
    password: str  

class Login(BaseModel):
    email: EmailStr  
    password: str 