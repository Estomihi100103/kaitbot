from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class DocumentCreate(BaseModel):
    title: str
    folder_id: Optional[int] = None

class DocEmbeddingSchema(BaseModel):
    id: int
    chunk_content: str
    extractmetadata: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class DocumentCreateResponse(BaseModel):
    id: int
    title: str
    file_type: str
    file_path: Optional[str]
    keywords_search: Optional[str]
    created_at: datetime
    company_id: int
    folder_id: Optional[int]

    class Config:
        from_attributes = True

class DocumentDetailResponse(DocumentCreateResponse):
    embeddings: List[DocEmbeddingSchema] = []

    class Config:
        from_attributes = True