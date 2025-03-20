from sqlalchemy.orm import Session
from entities import Budget

class BudgetRepository:

  @staticmethod
  def save(db: Session, budget: Budget) -> Budget:
    if budget.id:
        db.merge(budget)
    else:
        db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget

  @staticmethod
  def get_by(db: Session, key: str, value) -> Budget:
    if not hasattr(Budget, key):  # Verifica se o atributo existe na classe Budget
      raise ValueError(f"Column '{key}' does not exist in Budget model")

    return db.query(Budget).filter(getattr(Budget, key) == value).first()

  @staticmethod
  def get_all(db: Session) -> list[Budget]:
    return db.query(Budget).all()

  @staticmethod
  def find_by_id(db: Session, id: int) -> Budget:
    return db.query(Budget).filter(Budget.id == id).first()

  @staticmethod
  def delete_by_id(db: Session, id: int) -> None:
    budget = db.query(Budget).filter(Budget.id == id).first()

    if budget is not None:
      db.delete(budget)
      db.commit()

  @staticmethod
  def is_budget_exists(db: Session, id: int) -> bool:
    return db.query(Budget).filter(Budget.id == id).first() is not None

