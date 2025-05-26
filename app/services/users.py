from sqlalchemy.orm import Session
from app.validators.users import UserCreate, UserUpdate
from app.db.models.users import get_user_by_email, get_user_by_username, create_user as db_create_user, get_all_users, get_user_by_id, delete_user_by_id, update_user_db
from fastapi import HTTPException, status
from app.utils.security import hash_password

def create_user_service(db: Session, user_in: UserCreate):
    # Check if user exists by email or username
    if get_user_by_email(db, user_in.email):
        raise ValueError("Email is already in use.")

    if get_user_by_username(db, user_in.username):
        raise ValueError("Username is already taken.")

    # Hash the password
    hashed_pw = hash_password(user_in.password)

    # Create user in DB
    return db_create_user(
        db=db,
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_pw,
        role=user_in.role
    )

def list_users_service(db: Session):
    return get_all_users(db)

def get_user_service(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def delete_user_service(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    delete_user_by_id(db, user_id)

def update_user_service(db: Session, user_id: int, user_update: UserUpdate):
    return update_user_db(db, user_id, user_update)

