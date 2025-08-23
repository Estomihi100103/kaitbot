from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base


class UrlCompany(Base):
    __tablename__ = "url_companies"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)

    # relationships
    company = relationship("Company", back_populates="urls")
    web_embeddings = relationship("WebEmbedding", back_populates="url_company", cascade="all, delete-orphan")