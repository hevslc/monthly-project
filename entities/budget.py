from sqlalchemy import Column, Integer, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Budget(Base):
  __tablename__ = "budgets"

  id = Column(Integer, primary_key=True)
  category = Column(Enum("Alimentação", "Lazer", "Transporte", "Moradia", "Educação", "Outros"), nullable=False)
  limit_amount = Column(Float, nullable=False)  # Limite do orçamento
  created_at = Column(DateTime, default=datetime.utcnow)

  user = relationship("User", back_populates="budgets")
  user_id = Column(Integer, ForeignKey("users.id"))

