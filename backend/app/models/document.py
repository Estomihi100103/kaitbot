from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from datetime import datetime
from app.config.database import Base
from sqlalchemy.orm import relationship


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    keywords_search = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # foreign key ke company
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    company = relationship("Company", back_populates="documents")
    
    # foreign key ke folder
    folder_id = Column(Integer, ForeignKey("folders.id", ondelete="SET NULL"), nullable=True)
    folder = relationship("Folder", back_populates="documents")
    
    embeddings = relationship("DocEmbedding", back_populates="document", cascade="all, delete-orphan")
