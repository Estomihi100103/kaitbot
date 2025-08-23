
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.company import Company
from app.models.conversation import Conversation, Message, MessageSender
from app.schemas.conversation import ConversationResponse
from typing import List

router = APIRouter(prefix="/conversations", tags=["conversations"])

from pydantic import BaseModel
from datetime import datetime

class ConversationSummary(BaseModel):
    id: int
    thread_id: str
    created_at: datetime
    first_user_message: str | None = None
    last_message_preview: str | None = None
    message_count: int

# Endpoint untuk mendapatkan SEMUA percakapan milik sebuah company
@router.get("/by-company/{company_slug}", response_model=List[ConversationSummary])
def get_conversations_for_company(
    company_slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    company = db.query(Company).filter(Company.slug == company_slug, Company.user_id == current_user.id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    
    conversations = db.query(Conversation).filter(Conversation.company_id == company.id).order_by(Conversation.created_at.desc()).all()
    
    summaries = []
    for conv in conversations:
        first_message = db.query(Message).filter(Message.conversation_id == conv.id, Message.sender == MessageSender.USER).order_by(Message.created_at.asc()).first()
        last_message = db.query(Message).filter(Message.conversation_id == conv.id).order_by(Message.created_at.desc()).first()
        
        summaries.append(
            ConversationSummary(
                id=conv.id,
                thread_id=conv.thread_id,
                created_at=conv.created_at,
                first_user_message=first_message.content if first_message else "...",
                last_message_preview=f"{last_message.sender.name}: {last_message.content[:40]}..." if last_message else "...",
                message_count=len(conv.messages)
            )
        )
    return summaries


# Endpoint untuk mendapatkan DETAIL sebuah percakapan (termasuk semua pesan)
@router.get("/{thread_id}", response_model=ConversationResponse)
def get_conversation_detail(
    thread_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = db.query(Conversation).filter(Conversation.thread_id == thread_id).first()
    if not conversation or conversation.company.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    
    return conversation