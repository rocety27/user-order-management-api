from datetime import timedelta
from app.utils.jwt import create_access_token
from app.db.crud.auth import get_user_by_username, get_permissions_for_role
from sqlalchemy.orm import Session
from app.db.models import Rule
from datetime import timedelta
from app.utils.security import verify_password


def authenticate_user(db, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_permissions_for_role(db: Session, role_name: str) -> list[str]:
    permissions = (
        db.query(Rule.permission_name)
        .filter(Rule.role_name == role_name)
        .all()
    )
    return [perm.permission_name for perm in permissions]


def create_token_for_user(db: Session, user):
    permissions = get_permissions_for_role(db, user.role_name)

    token_data = {
        "sub": str(user.id),
        "role": user.role_name,
        "permissions": permissions,
    }

    expires_delta = timedelta(minutes=15)
    access_token = create_access_token(token_data, expires_delta)
    return access_token
