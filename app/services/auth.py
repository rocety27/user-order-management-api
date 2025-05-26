from passlib.context import CryptContext
from datetime import timedelta
from app.utils.jwt import create_access_token
from app.services.users import get_user_by_username

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_token_for_user(user):
    token_data = {"user_id": user.id, "role": user.role}
    access_token_expires = timedelta(minutes=60)
    token = create_access_token(token_data, expires_delta=access_token_expires)
    return token
