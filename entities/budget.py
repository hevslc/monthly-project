from sqlalchemy import Column, Integer, Float, ForeignKey, Enum, DateTime
from datetime import datetime
from database import Base

class Budget(Base):
  __tablename__ = "budgets"

  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  category = Column(Enum("Alimentação", "Lazer", "Transporte", "Moradia", "Educação", "Outros"), nullable=False)
  limit_amount = Column(Float, nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow)
