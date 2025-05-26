# --- User Endpoints ---

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.validators.users import UserCreate, UserOut
from app.services.users import create_user_service
from app.services.users import list_users_service
from typing import List


router = APIRouter()

@router.post("/", summary="Create a new user (Admin only)", response_model=UserOut)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user_service(db, user_in)
        return user
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        print(f"Unexpected error: {e}")  # Log error here
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred.")

@router.get("/", summary="List all users (Admin only)", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    try:
        users = list_users_service(db)
        return users
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred.")


@router.get("/me", summary="Get current user's profile")
def get_me():
    # Customer only
    pass

@router.put("/me", summary="Update current user's profile")
def update_me(user_update: dict):
    # Customer only
    pass

@router.get("/{user_id}", summary="Get user by ID")
def get_user(user_id: int):
    # Admin or Customer (own)
    pass

@router.put("/{user_id}", summary="Update user by ID")
def update_user(user_id: int, user_update: dict):
    # Admin or Customer (own)
    pass

@router.delete("/{user_id}", summary="Delete user by ID")
def delete_user(user_id: int):
    # Admin only
    pass

@router.get("/{user_id}/orders", summary="List orders by user (Admin only)")
def list_user_orders(user_id: int):
    # Admin only
    pass