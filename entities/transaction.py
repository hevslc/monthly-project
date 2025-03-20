from sqlalchemy import Column, Integer, Float, ForeignKey, Enum, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Transaction(Base):
  __tablename__ = "transactions"

  id = Column(Integer, primary_key=True)
  category = Column(Enum("Alimentação", "Lazer", "Transporte", "Moradia", "Educação", "Outros"), nullable=False)
  amount = Column(Float, nullable=False)
  transaction_type = Column(Enum("Entrada", "Saída"), nullable=False)
  description = Column(String, nullable=True)
  date = Column(DateTime, default=datetime.utcnow)

  user = relationship("User", back_populates="transactions")
  user_id = Column(Integer, ForeignKey("users.id"))
