from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import db_session
from repositories import TransactionRepository
from models import TransactionResponse, TransactionRequest
from entities import Transaction

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=TransactionResponse)
def create_transaction(transaction_data: TransactionRequest, db: Session = Depends(db_session)):
  transaction = TransactionRepository.save(db, Transaction(**transaction_data.dict()))
  return TransactionResponse.model_validate(transaction)

@router.get("/{id}", response_model=TransactionResponse)
def get_transaction(id: int, db: Session = Depends(db_session)):
  transaction = TransactionRepository.find_by_id(db, id)

  if not transaction:
    raise HTTPException(status_code=404, detail="Operação não encontrada")

  return TransactionResponse.model_validate(transaction)

@router.get("/", response_model=list[TransactionResponse])
def list_transactions(db: Session = Depends(db_session)):
  transactions = TransactionRepository.get_all(db)
  return [TransactionResponse.model_validate(transaction) for transaction in transactions]

@router.delete("/{id}")
def delete_transaction(id: int, db: Session = Depends(db_session)):
  transaction = TransactionRepository.is_transaction_exists(db, id)

  if not transaction:
    raise HTTPException(status_code=404, detail="Operação não encontrada")

  TransactionRepository.delete_by_id(db, id)
  return {"message": "Operação removida com sucesso"}

@router.put("/{id}", response_model=TransactionResponse)
def update(id: int, request: TransactionRequest, db: Session = Depends(db_session)):
  transaction = TransactionRepository.find_by_id(db, id)

  if not transaction:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="Operação não encontrado"
    )

  update_data = request.model_dump(exclude_unset=True)

  for key, value in update_data.items():
    setattr(transaction, key, value)

  transaction = TransactionRepository.save(db, transaction)
  return TransactionResponse.model_validate(transaction)
