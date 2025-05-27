from sqlalchemy.orm import Session
from app.db.models.orders import Order

def get_order_by_id(db: Session, order_id: int) -> Order | None:
    return db.query(Order).filter(Order.id == order_id).first()

def create_order(db: Session, user_id: int, total_amount, status: str = "pending") -> Order:
    order = Order(user_id=user_id, total_amount=total_amount, status=status)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_orders_by_user_id(db: Session, user_id: int) -> list[Order]:
    return db.query(Order).filter(Order.user_id == user_id).all()

def delete_order_by_id(db: Session, order_id: int):
    order = get_order_by_id(db, order_id)
    if order:
        db.delete(order)
        db.commit()
