from pydantic import BaseModel, condecimal
from typing import Literal
from datetime import datetime

class TransactionBase(BaseModel):
  category: str
  amount: condecimal(max_digits=10, decimal_places=2)
  transaction_type: Literal["Entrada", "Saída"]

class TransactionRequest(TransactionBase):
  user_id: int  # ID do usuário que fez a transação

class TransactionResponse(TransactionBase):
  id: int
  created_at: datetime

  class Config:
    from_attributes = True
