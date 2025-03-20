from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import db_session
from repositories import UserRepository
from models import UserResponse, UserRequest
from entities import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user(user_data: UserRequest, db: Session = Depends(db_session)):
  user = User(**user_data.dict())
  return UserRepository.save(db, user)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(db_session)):
  user = UserRepository.find_by_id(db, user_id)
  if not user:
    raise HTTPException(status_code=404, detail="Usuário não encontrado")
  return user

@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(db_session)):
  return UserRepository.get_all(db)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(db_session)):
  user = UserRepository.find_by_id(db, user_id)
  if not user:
    raise HTTPException(status_code=404, detail="Usuário não encontrado")
  UserRepository.delete_by_id(db, user_id)
  return {"message": "Usuário removido com sucesso"}

@router.put("/{user_id}", response_model=UserResponse)
def update(id: int, request: UserRequest, db: Session = Depends(db_session)):
  if not UserRepository.is_user_exists(db, id):
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
    )
  user = UserRepository.save(db, User(id=id, **request.dict()))
  return UserResponse.from_orm(user)