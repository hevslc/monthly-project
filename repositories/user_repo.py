from sqlalchemy.orm import Session
from entities import User

class UserRepository:

  @staticmethod
  def save(db: Session, user: User) -> User:
    if user.id:
        db.merge(user)
    else:
        db.add(user)
    db.commit()
    db.refresh(user)
    return user

  @staticmethod
  def get_by(db: Session, key: str, value) -> User:
    if not hasattr(User, key):  # Verifica se o atributo existe na classe User
      raise ValueError(f"Column '{key}' does not exist in User model")

    return db.query(User).filter(getattr(User, key) == value).first()

  @staticmethod
  def get_all(db: Session) -> list[User]:
    return db.query(User).all()

  @staticmethod
  def find_by_id(db: Session, id: int) -> User:
    return db.query(User).filter(User.id == id).first()

  @staticmethod
  def delete_by_id(db: Session, id: int) -> None:
    user = db.query(User).filter(User.id == id).first()

    if user is not None:
      db.delete(user)
      db.commit()
  
  @staticmethod
  def is_user_exists(db: Session, id: int) -> bool:
    return db.query(User).filter(User.id == id).first() is not None
