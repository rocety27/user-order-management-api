from app.db.session import SessionLocal
from app.db.models.roles import Role
from app.db.models.permissions import Permission
from app.db.models.rules import Rule
from app.db.models.users import User
from app.utils.hashing import hash_password

import os
from dotenv import load_dotenv
load_dotenv()

def seed_roles(db):
    roles = [
        Role(name="admin"),
        Role(name="customer"),
        # add more roles if needed
    ]
    for role in roles:
        existing = db.query(Role).filter(Role.name == role.name).first()
        if not existing:
            db.add(role)
    db.commit()


def seed_permissions(db):
    permissions = [
        # User related permissions
        Permission(name="can_create_user"),
        Permission(name="can_list_users"),
        Permission(name="can_get_user"),
        Permission(name="can_update_user"),
        Permission(name="can_delete_user"),
        
        #Permission(name="can_get_own_profile"),
        #Permission(name="can_update_own_profile"),
    ]
    for perm in permissions:
        existing = db.query(Permission).filter(Permission.name == perm.name).first()
        if not existing:
            db.add(perm)
    db.commit()


def seed_rules(db):
    # Fetch roles
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    customer_role = db.query(Role).filter(Role.name == "customer").first()

    # Fetch permissions
    can_create_user = db.query(Permission).filter(Permission.name == "can_create_user").first()
    can_list_users = db.query(Permission).filter(Permission.name == "can_list_users").first()
    can_get_user = db.query(Permission).filter(Permission.name == "can_get_user").first()
    can_update_user = db.query(Permission).filter(Permission.name == "can_update_user").first()
    can_delete_user = db.query(Permission).filter(Permission.name == "can_delete_user").first()

    rules = [
        # Admin permissions - full user management
        Rule(role_id=admin_role.id, permission_id=can_create_user.id),
        Rule(role_id=admin_role.id, permission_id=can_list_users.id),
        Rule(role_id=admin_role.id, permission_id=can_get_user.id),
        Rule(role_id=admin_role.id, permission_id=can_update_user.id),
        Rule(role_id=admin_role.id, permission_id=can_delete_user.id),

        # Customer permissions - maybe limited or none here
        # Rule(role_id=customer_role.id, permission_id=can_get_own_profile.id),
        # Rule(role_id=customer_role.id, permission_id=can_update_own_profile.id),
    ]

    for rule in rules:
        existing = db.query(Rule).filter(
            Rule.role_id == rule.role_id,
            Rule.permission_id == rule.permission_id
        ).first()
        if not existing:
            db.add(rule)

    db.commit()



def seed_admin_user(db):
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    existing_admin = db.query(User).filter(User.role_name == admin_role.name).first()
    if existing_admin:
        print("Admin user already exists, skipping creation.")
        return

    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "adminpassword123")

    admin_user = User(
        username=admin_username,
        email=admin_email,
        hashed_password=hash_password(admin_password),
        role_name=admin_role.name
    )
    db.add(admin_user)
    db.commit()
    print("Admin user created.")

def seed_all():
    db = SessionLocal()
    try:
        seed_roles(db)
        seed_permissions(db)
        seed_rules(db)
        seed_admin_user(db)
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()
