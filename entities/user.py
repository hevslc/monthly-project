
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
  __tablename__ = 'users'
  
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  email = Column(String, unique=True, nullable=False)
  password_hash = Column(String, nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow)

  transactions = relationship("Transaction", back_populates="user")
  budgets = relationship("Budget", back_populates="user")

