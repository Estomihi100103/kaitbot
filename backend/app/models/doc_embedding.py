from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Index
from pgvector.sqlalchemy import Vector
from datetime import datetime
from app.config.database import Base 
from sqlalchemy.orm import relationship


class DocEmbedding(Base):
    __tablename__ = "doc_embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    chunk_content = Column(Text, nullable=False)
    embedding = Column(Vector(1536), nullable=False) 
    extractmetadata = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)

    # relationships
    document = relationship("Document", back_populates="embeddings")
    company = relationship("Company", back_populates="embeddings")

    #defenisikan index
    __table_args__=(
        Index(
            'ix_doc_embeddings_embedding',                      # nama index
            'embedding',                                        # nama kolom yang di index
             postgresql_using='hnsw',
             postgresql_with={'m': 16, 'ef_construction': 64},  # tipe index
             postgresql_ops={'embedding': 'vector_l2_ops'}
        ),
    )