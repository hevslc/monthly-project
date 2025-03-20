from pydantic import BaseModel, condecimal
from datetime import datetime

class BudgetBase(BaseModel):
  category: str
  limit_amount: condecimal(max_digits=10, decimal_places=2)

class BudgetRequest(BudgetBase):
  user_id: int  # ID do usuário que criou o orçamento

class BudgetResponse(BudgetBase):
  id: int
  created_at: datetime

  class Config:
    from_attributes = True
