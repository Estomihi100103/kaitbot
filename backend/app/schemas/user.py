from pydantic import BaseModel
from datetime import datetime
from app.schemas.company import CompanyResponse
from typing import Optional, List

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    companies: Optional[list[CompanyResponse]] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str