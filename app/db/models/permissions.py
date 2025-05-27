from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Permission(Base):
    __tablename__ = "permissions"

    name = Column(String(100), primary_key=True)
    rules = relationship("Rule", back_populates="permission", cascade="all, delete-orphan")
