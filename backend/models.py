from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str]=None
    company: Optional[str]=None
    is_verified: bool=False
    
class Otp(BaseModel):
    email : EmailStr
    otp: str
    