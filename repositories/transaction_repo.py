from sqlalchemy.orm import Session
from entities import Transaction

class TransactionRepository:

  @staticmethod
  def save(db: Session, transaction: Transaction) -> Transaction:
    if transaction.id:
        db.merge(transaction)
    else:
        db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

  @staticmethod
  def get_by(db: Session, key: str, value) -> Transaction:
    if not hasattr(Transaction, key):  # Verifica se o atributo existe na classe Transaction
      raise ValueError(f"Column '{key}' does not exist in Transaction model")

    return db.query(Transaction).filter(getattr(Transaction, key) == value).first()

  @staticmethod
  def get_all(db: Session) -> list[Transaction]:
    return db.query(Transaction).all()

  @staticmethod
  def find_by_id(db: Session, id: int) -> Transaction:
    return db.query(Transaction).filter(Transaction.id == id).first()

  @staticmethod
  def delete_by_id(db: Session, id: int) -> None:
    transaction = db.query(Transaction).filter(Transaction.id == id).first()

    if transaction is not None:
      db.delete(transaction)
      db.commit()
  
  @staticmethod
  def is_transaction_exists(db: Session, id: int) -> bool:
    return db.query(Transaction).filter(Transaction.id == id).first() is not None
