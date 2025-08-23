from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Index 
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base


class WebEmbedding(Base):
    __tablename__ = "web_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1536), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    url_company_id = Column(Integer, ForeignKey("url_companies.id", ondelete="CASCADE"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)

    # relationships
    url_company = relationship("UrlCompany", back_populates="web_embeddings")
    company = relationship("Company", back_populates="web_embeddings")
    
    __table_args__ = (
        Index(
            'ix_web_embeddings_embedding',     
            'embedding',                        
            postgresql_using='hnsw',            
            postgresql_with={'m': 16, 'ef_construction': 64},
            postgresql_ops={'embedding': 'vector_l2_ops'}
        ),
    )