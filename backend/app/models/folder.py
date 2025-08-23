from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from datetime import datetime
from app.config.database import Base
from sqlalchemy.orm import relationship

class Folder(Base):
    __tablename__ = "folders"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # foreign key ke company
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    company = relationship("Company", back_populates="folders")
    
    # relationships
    documents = relationship("Document", back_populates="folder", cascade="all, delete-orphan")
