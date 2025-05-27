from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.db.models.orders import Order

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="customer")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    orders = relationship(Order, back_populates="user", cascade="all, delete-orphan")
