from pydantic import BaseModel
from datetime import datetime
from typing import List

from app.models.conversation import MessageSender

class MessageBase(BaseModel):
    content: str
    sender: MessageSender

class MessageResponse(MessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: int
    thread_id: str
    created_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True