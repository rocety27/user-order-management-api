from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from typing import List

from sqlalchemy.orm import Session
from app.db.session import get_db

from app.validators.users import UserCreate, UserUpdate, UserOut
from app.validators.auth import TokenData

from app.services.users import (
    create_user_service,
    list_users_service,
    get_user_service,
    delete_user_service,
    update_user_service,
)

from app.utils.jwt import (
    get_current_user,
    permission_required,
)

router = APIRouter()

@router.post("/", summary="Create a new user", response_model=UserOut)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(permission_required("can_create_user")),
):
    try:
        user = create_user_service(db, user_in)
        return user
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred.",
        )

@router.get("/", summary="List all users", response_model=List[UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(permission_required("can_list_users")),
):
    try:
        users = list_users_service(db)
        return users
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred.",
        )

@router.get("/me", summary="Get current user's profile", response_model=UserOut)
def get_me(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    try:
        user = get_user_service(db, current_user.user_id)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred.",
        )

@router.put("/me", summary="Update current user's profile", response_model=UserOut)
def update_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    try:
        user = update_user_service(db, current_user.user_id, user_update)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred.",
        )

@router.get("/{user_id}", summary="Get user by ID", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    if "get_any_user" not in current_user.permissions and current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied.",
        )
    try:
        user = get_user_service(db, user_id)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred.",
        )

@router.put("/{user_id}", summary="Update user by ID", response_model=UserOut)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    if "update_any_user" not in current_user.permissions and current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied.",
        )
    try:
        user = update_user_service(db, user_id, user_update)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred.",
        )

@router.delete("/{user_id}", summary="Delete user by ID", status_code=200)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(permission_required("delete_user")),
):
    try:
        delete_user_service(db, user_id)
        return JSONResponse(
            content={"message": f"User with ID {user_id} deleted successfully."}
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred.",
        )


# @router.get("/{user_id}/orders", summary="List orders by user (Admin only)")
# def list_user_orders(
#     user_id: int, current_user: TokenData = Depends(admin_required)
# ):
#     # Implement orders fetching logic here, admin only
#     pass
