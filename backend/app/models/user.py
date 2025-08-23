from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.config.database import Base 
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # relationships
    companies = relationship("Company", back_populates="owner", cascade="all, delete-orphan")