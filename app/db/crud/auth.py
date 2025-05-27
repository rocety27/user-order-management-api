from sqlalchemy.orm import Session
from app.db.models.users import User
from app.db.models.rules import Rule

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

def get_permissions_for_role(db: Session, role_name: str) -> list[str]:
    permissions = (
        db.query(Rule.permission_name)
        .filter(Rule.role_name == role_name)
        .all()
    )
    return [perm.permission_name for perm in permissions]
