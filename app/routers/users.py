from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

router = APIRouter()

# --- User Endpoints ---

@router.post("/", summary="Create a new user (Admin only)")
def create_user(user_in: dict):
    # Only Admins allowed
    pass

@router.get("/", summary="List all users (Admin only)")
def list_users():
    # Only Admins allowed
    pass

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