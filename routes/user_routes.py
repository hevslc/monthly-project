from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import db_session
from repositories import UserRepository
from models import UserResponse, UserRequest, UserUpdate
from entities import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user(user_data: UserRequest, db: Session = Depends(db_session)):
  user = UserRepository.save(db, User(**user_data.dict()))
  return UserResponse.model_validate(user)

@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(db_session)):
  user = UserRepository.find_by_id(db, id)

  if not user:
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

  return UserResponse.model_validate(user)

@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(db_session)):
  users = UserRepository.get_all(db)
  return [UserResponse.model_validate(user) for user in users]

@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(db_session)):
  user = UserRepository.is_user_exists(db, id)

  if not user:
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

  UserRepository.delete_by_id(db, id)
  return {"message": "Usuário removido com sucesso"}

@router.put("/{id}", response_model=UserResponse)
def update(id: int, request: UserUpdate, db: Session = Depends(db_session)):
  user = UserRepository.find_by_id(db, id)

  if not user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
    )

  update_data = request.model_dump(exclude_unset=True)

  for key, value in update_data.items():
    setattr(user, key, value)

  user = UserRepository.save(db, user)
  return UserResponse.model_validate(user)