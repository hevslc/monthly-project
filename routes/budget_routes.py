from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import db_session
from repositories.budget_repo import BudgetRepository
from models import BudgetRequest, BudgetResponse
from entities import Budget

router = APIRouter(prefix="/budgets", tags=["Budgets"])

@router.post("/", response_model=BudgetResponse)
def create_budget(budget_data: BudgetRequest, db: Session = Depends(db_session)):
  budget = BudgetRepository.save(db, Budget(**budget_data.dict()))
  return BudgetResponse.model_validate(budget)

@router.get("/{id}", response_model=BudgetResponse)
def get_budget(id: int, db: Session = Depends(db_session)):
  budget = BudgetRepository.find_by_id(db, id)

  if not budget:
    raise HTTPException(status_code=404, detail="Orçamento não encontrado")
  return BudgetResponse.model_validate(budget)

@router.get("/", response_model=list[BudgetResponse])
def list_budgets(db: Session = Depends(db_session)):
  budgets = BudgetRepository.get_all(db)
  return [BudgetResponse.model_validate(budget) for budget in budgets]

@router.delete("/{id}")
def delete_budget(id: int, db: Session = Depends(db_session)):
  budget = BudgetRepository.is_budget_exists(db, id)

  if not budget:
    raise HTTPException(status_code=404, detail="Orçamento não encontrado")

  BudgetRepository.delete_by_id(db, id)
  return {"message": "Orçamento removido com sucesso"}

@router.put("/{id}", response_model=BudgetResponse)
def update(id: int, request: BudgetRequest, db: Session = Depends(db_session)):
  budget = BudgetRepository.find_by_id(db, id)

  if not budget:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="Orçamento não encontrado"
    )
  
  update_data = request.model_dump(exclude_unset=True)

  for key, value in update_data.items():
    setattr(budget, key, value)

  budget = BudgetRepository.save(db, budget)
  return BudgetResponse.model_validate(budget)