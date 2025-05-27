from sqlalchemy.orm import Session
from app.db.models import User, Rule

def get_user_by_username(db: Session, username: str) -> User | None:
    print("Debug: Listing all users in the database:")
    all_users = db.query(User).all()
    for user in all_users:
        print(f" - id={user.id}, username={user.username}, email={user.email}, role={user.role_name}")
    
    print(f"Debug: Searching for user with username='{username}'")
    user = db.query(User).filter(User.username == username).first()
    if user:
        print(f"Debug: Found user with id={user.id}")
    else:
        print("Debug: No user found")
    return user


def get_permissions_for_role(db: Session, role_name: str) -> list[str]:
    permissions = (
        db.query(Rule.permission_name)
        .filter(Rule.role_name == role_name)
        .all()
    )
    return [perm.permission_name for perm in permissions]
