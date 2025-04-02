from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import Optional
from datetime import date, datetime

class User(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str]=None
    company: Optional[str]=None
    is_verified: bool=False
    
class Otp(BaseModel):
    email : EmailStr
    otp: str
    
    
class Ipo(BaseModel):
    category: str  # upcoming, listed, active, closed
    symbol: str 
    name: str
    status: str
    is_sme: bool
    additional_text: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    issue_price: Optional[float] = None
    listing_gains: Optional[float] = None
    listing_price: Optional[float] = None
    bidding_start_date: Optional[date] = None
    bidding_end_date: Optional[date] = None
    listing_date: Optional[date] = None
    lot_size: Optional[int] = None
    # document_url: str  
    last_updated: datetime = Field(default_factory=datetime.utcnow)