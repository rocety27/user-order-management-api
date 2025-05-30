import os
import datetime
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from app.validators.auth import TokenData
from typing import Callable

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_token(data: dict, expires_delta: datetime.timedelta) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.datetime.utcnow() + expires_delta
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def create_access_token(user: dict) -> str:
    return create_token(
        data={
            "sub": str(user["id"]),
            "role": user["role"],
            "permissions": user.get("permissions", []),
            "type": "access"
        },
        expires_delta=datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_refresh_token(user: dict) -> str:
    return create_token(
        data={
            "sub": str(user["id"]),
            "type": "refresh"
        },
        expires_delta=datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=400, detail="Invalid token type")
    
    user_id = int(payload.get("sub"))
    role = payload.get("role")
    permissions = payload.get("permissions", [])

    if user_id is None or role is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return TokenData(user_id=user_id, role=role, permissions=permissions)


def permission_required(permission: str) -> Callable:
    def _permission_dependency(current_user: TokenData = Depends(get_current_user)) -> TokenData:
        if permission not in current_user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission}' required."
            )
        return current_user
    return _permission_dependency