from pydantic import BaseModel, EmailStr
from typing import Optional

class AttendeeRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    event_id: int


class UpdateCheckInStatus(BaseModel):
    status: bool