from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models import User
from app.validators.users import UserUpdate

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_all_users(db: Session):
    return db.query(User).all()


def create_user(db: Session, username: str, email: str, hashed_password: str, role: str = "customer") -> User:
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        role_name=role
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_db(db: Session, user_id: int, user_update: UserUpdate):
    user = get_user_by_id(db, user_id)
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


def delete_user_by_id(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()