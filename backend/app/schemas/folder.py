from pydantic import BaseModel
from typing import List
from datetime import datetime

class FolderBase(BaseModel):
    name: str

class FolderCreate(FolderBase):
    pass

class Folder(FolderBase):
    id: int
    company_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FolderWithDocs(Folder):
    document_count: int
    documents: List["DocumentCreateResponse"]

from app.schemas.document import DocumentCreateResponse
FolderWithDocs.model_rebuild()