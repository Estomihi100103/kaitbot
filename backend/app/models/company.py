from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base
from sqlalchemy.dialects.postgresql import JSONB 


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    greeting_message = Column(Text, nullable=True, default="Halo! Bagaimana saya bisa membantu Anda?")
    style_config = Column(JSONB, nullable=True, default=lambda: {"primaryColor": "#007bff", "position": "bottom-right"})

    # relationships
    owner = relationship("User", back_populates="companies")
    folders = relationship("Folder", back_populates="company", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="company", cascade="all, delete-orphan")
    urls = relationship("UrlCompany", back_populates="company", cascade="all, delete-orphan")
    embeddings = relationship("DocEmbedding", back_populates="company", cascade="all, delete-orphan")
    web_embeddings = relationship("WebEmbedding", back_populates="company", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="company", cascade="all, delete-orphan")