from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import db_session
from repositories.budget_repo import BudgetRepository
from models import BudgetRequest, BudgetResponse
from entities import Budget

router = APIRouter(prefix="/budgets", tags=["Budgets"])

@router.post("/", response_model=BudgetResponse)
def create_budget(budget_data: BudgetRequest, db: Session = Depends(db_session)):
  budget = Budget(**budget_data.dict())
  return BudgetRepository.save(db, budget)

@router.get("/{budget_id}", response_model=BudgetResponse)
def get_budget(budget_id: int, db: Session = Depends(db_session)):
  budget = BudgetRepository.find_by_id(db, budget_id)
  if not budget:
    raise HTTPException(status_code=404, detail="Orçamento não encontrado")
  return budget

@router.get("/", response_model=list[BudgetResponse])
def list_budgets(db: Session = Depends(db_session)):
  return BudgetRepository.get_all(db)

@router.delete("/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(db_session)):
  budget = BudgetRepository.find_by_id(db, budget_id)
  if not budget:
    raise HTTPException(status_code=404, detail="Orçamento não encontrado")
  BudgetRepository.delete_by_id(db, budget_id)
  return {"message": "Orçamento removido com sucesso"}

@router.put("/{budget_id}", response_model=BudgetResponse)
def update(id: int, request: BudgetRequest, db: Session = Depends(db_session)):
  if not BudgetRepository.is_budget_exists(db, id):
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="Orçamento não encontrado"
    )
  budget = BudgetRepository.save(db, Budget(id=id, **request.dict()))
  return BudgetResponse.from_orm(budget)