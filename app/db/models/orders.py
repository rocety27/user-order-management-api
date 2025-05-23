from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import relationship, Session
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_date = Column(DateTime, server_default=func.now())
    total_amount = Column(Numeric, nullable=False)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="orders")

# --- DB interaction functions ---

def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def create_order(db: Session, user_id: int, total_amount, status: str = "pending"):
    order = Order(user_id=user_id, total_amount=total_amount, status=status)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order