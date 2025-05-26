from sqlalchemy.orm import Session
from schemas.user import UserCreate
from crud.user import get_user_by_email, get_user_by_username, create_user as db_create_user
from utils.security import hash_password  # make sure this exists

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
