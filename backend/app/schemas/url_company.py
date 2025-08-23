from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UrlCompanyBase(BaseModel):
    url: str

class UrlCompanyCreate(UrlCompanyBase):
    pass

class UrlCompany(UrlCompanyBase):
    id: int
    company_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UrlCompanyCreateRequest(BaseModel):
    urls: list[str]