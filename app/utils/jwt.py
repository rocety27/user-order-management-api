import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from app.validators.users import TokenData

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret")  # Use env var in prod
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # URL for token endpoint

def create_access_token(data: dict, expires_delta=None):
    import datetime
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: int = payload.get("user_id")
        role: str = payload.get("role")
        if user_id is None or role is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, role=role)
    except PyJWTError:
        raise credentials_exception
    return token_data

def admin_required(current_user: TokenData = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required.",
        )
    return current_user
