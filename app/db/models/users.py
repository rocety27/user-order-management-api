from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship, Session 
from app.db.models.orders import Order
from app.db.base import Base
from fastapi import HTTPException, status
from app.validators.users import UserUpdate

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="customer")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    orders = relationship(Order, back_populates="user", cascade="all, delete-orphan")

# --- DB interaction functions ---

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, email: str, hashed_password: str, role: str = "customer") -> User:
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_all_users(db: Session):
    return db.query(User).all()

def delete_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()

def update_user_db(db: Session, user_id: int, user_update: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    if user_update.username is not None:
        user.username = user_update.username
    if user_update.email is not None:
        user.email = user_update.email

    db.commit()
    db.refresh(user)
    return user

