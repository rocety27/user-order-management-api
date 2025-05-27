# app/db/models/role.py
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Role(Base):
    __tablename__ = "roles"

    name = Column(String(50), primary_key=True)  # e.g. "admin", "customer"
    users = relationship("User", back_populates="role")
    rules = relationship("Rule", back_populates="role", cascade="all, delete-orphan")
