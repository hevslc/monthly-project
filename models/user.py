from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
  name: str
  email: EmailStr
  password_hash: str

class UserRequest(UserBase):
  pass

class UserUpdate(BaseModel):
  name: Optional[str] = None
  email: Optional[EmailStr] = None
  password_hash: Optional[str] = None

class UserResponse(UserBase):
  id: int
  created_at: datetime

  class Config:
    from_attributes = True  # Permite converter de um objeto SQLAlchemy para Pydantic
