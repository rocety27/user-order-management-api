from app.db.session import SessionLocal
from app.db.models.roles import Role
from app.db.models.permissions import Permission
from app.db.models import Rule, User
from app.utils.security import hash_password

import os
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv() # Load environment variables from .env file

def clear_tables(db):
    # Truncate with restart identity to reset auto-increment IDs
    db.execute(text("TRUNCATE TABLE rules, permissions, roles, users RESTART IDENTITY CASCADE"))
    db.commit()


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
        Permission(name="can_get_own_profile"),
        Permission(name="can_update_own_profile"),

        # Order related permissions
        Permission(name="can_create_order"),
        Permission(name="can_list_orders"),
        Permission(name="can_get_order"),
        Permission(name="can_update_order"),
        Permission(name="can_delete_order"),

        Permission(name="can_get_own_orders"),
        Permission(name="can_get_own_order"),
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

    # # Fetch all permissions at once
    # permission_lookup = {
    #     perm.name: perm for perm in db.query(Permission).all()
    # }

    rules = [
        # Admin - User Management
        Rule(role_name=admin_role.name, permission_name="can_create_user"),
        Rule(role_name=admin_role.name, permission_name="can_list_users"),
        Rule(role_name=admin_role.name, permission_name="can_get_user"),
        Rule(role_name=admin_role.name, permission_name="can_update_user"),
        Rule(role_name=admin_role.name, permission_name="can_delete_user"),
        
        # Admin - Order Management
        Rule(role_name=admin_role.name, permission_name="can_create_order"),
        Rule(role_name=admin_role.name, permission_name="can_list_orders"),
        Rule(role_name=admin_role.name, permission_name="can_get_order"),
        Rule(role_name=admin_role.name, permission_name="can_update_order"),
        Rule(role_name=admin_role.name, permission_name="can_delete_order"),

        # Customer - Profile Management
        Rule(role_name=customer_role.name, permission_name="can_get_own_profile"),
        Rule(role_name=customer_role.name, permission_name="can_update_own_profile"),
        
        # Customer - Order Management
        Rule(role_name=customer_role.name, permission_name="can_create_order"),
        Rule(role_name=customer_role.name, permission_name="can_get_own_orders"),
        Rule(role_name=customer_role.name, permission_name="can_get_own_order"),
    ]

    for rule in rules:
        existing = db.query(Rule).filter(
            Rule.role_name == rule.role_name,
            Rule.permission_name == rule.permission_name
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


def seed_customer_users(db, n=3):
    customer_role = db.query(Role).filter(Role.name == "customer").first()
    
    customer_usernames = [f"customer{x}" for x in range(1, n+1)]
    customer_emails = [f"customer{x}@example.com" for x in range(1,n+1)]
    customer_passwords = [f"password{x}" for x in range(1, n+1)]

    for customer_username, customer_email, customer_password in zip(customer_usernames, customer_emails, customer_passwords):
        customer_user = User(
            username=customer_username,
            email=customer_email,
            hashed_password=hash_password(customer_password),
            role_name=customer_role.name
        )
        db.add(customer_user)
        db.commit()
        print("Customer user created.")


def seed_all():
    db = SessionLocal()
    try:
        clear_tables(db)  
        seed_roles(db)
        seed_permissions(db)
        seed_rules(db)
        seed_admin_user(db)
        seed_customer_users(db, n=3)

    finally:
        db.close()


if __name__ == "__main__":
    seed_all()
