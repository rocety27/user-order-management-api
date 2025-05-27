from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Rule(Base):
    __tablename__ = "rules"

    role_name = Column(String(50), ForeignKey("roles.name"), primary_key=True)
    permission_name = Column(String(100), ForeignKey("permissions.name"), primary_key=True)

    role = relationship("Role", back_populates="rules")
    permission = relationship("Permission", back_populates="rules")
