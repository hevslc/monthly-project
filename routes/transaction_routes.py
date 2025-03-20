from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import db_session
from repositories import TransactionRepository
from models import TransactionResponse, TransactionRequest
from entities import Transaction

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=TransactionResponse)
def create_transaction(transaction_data: TransactionRequest, db: Session = Depends(db_session)):
  transaction = Transaction(**transaction_data.dict())
  return TransactionRepository.save(db, transaction)

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(db_session)):
  transaction = TransactionRepository.find_by_id(db, transaction_id)
  if not transaction:
    raise HTTPException(status_code=404, detail="Operação não encontrada")
  return transaction

@router.get("/", response_model=list[TransactionResponse])
def list_transactions(db: Session = Depends(db_session)):
  return TransactionRepository.get_all(db)

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(db_session)):
  transaction = TransactionRepository.find_by_id(db, transaction_id)
  if not transaction:
    raise HTTPException(status_code=404, detail="Operação não encontrada")
  TransactionRepository.delete_by_id(db, transaction_id)
  return {"message": "Operação removida com sucesso"}

@router.put("/{transaction_id}", response_model=TransactionResponse)
def update(id: int, request: TransactionRequest, db: Session = Depends(db_session)):
  if not TransactionRepository.is_transaction_exists(db, id):
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="Operação não encontrado"
    )
  transaction = TransactionRepository.save(db, Transaction(id=id, **request.dict()))
  return TransactionResponse.from_orm(transaction)
