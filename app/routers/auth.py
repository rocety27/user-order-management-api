from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.auth import authenticate_user, get_permissions_for_role
from app.utils.jwt import create_access_token, create_refresh_token, decode_token
from app.db.models import User
from app.validators.auth import RefreshTokenRequest

router = APIRouter()

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Fetch permissions for user's role from DB
    permissions = get_permissions_for_role(db, user.role_name)

    user_data = {
        "id": user.id,
        "role": user.role_name,
        "permissions": permissions,
    }

    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    payload = decode_token(data.refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=400, detail="Invalid token type")

    user_id = int(payload.get("sub"))

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    permissions = get_permissions_for_role(db, user.role_name)

    user_data = {
        "id": user.id,
        "role": user.role_name,
        "permissions": permissions,
    }

    new_access_token = create_access_token(user_data)
    return {"access_token": new_access_token, "token_type": "bearer"}
