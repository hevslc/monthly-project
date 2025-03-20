from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
  name: str
  email: EmailStr

class UserRequest(UserBase):
  pass

class UserResponse(UserBase):
  id: int
  created_at: datetime

  class Config:
    from_attributes = True  # Permite converter de um objeto SQLAlchemy para Pydantic
