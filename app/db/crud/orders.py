from sqlalchemy.orm import Session
from app.db.models import Order
from app.validators.orders import OrderUpdate

def get_order_by_id(db: Session, order_id: int) -> Order | None:
    return db.query(Order).filter(Order.id == order_id).first()


def create_order(db: Session, user_id: int, total_amount: float, status: str = "pending") -> Order:
    order = Order(user_id=user_id, total_amount=total_amount, status=status)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_all_orders(db: Session) -> list[Order]:
    return db.query(Order).all()


def get_orders_by_user_id(db: Session, user_id: int) -> list[Order]:
    return db.query(Order).filter(Order.user_id == user_id).all()


def update_order_db(db: Session, order_id: int, order_update: OrderUpdate) -> Order:
    order = get_order_by_id(db, order_id)
    if not order:
        return None

    # Update allowed fields only
    for field, value in order_update.dict(exclude_unset=True).items():
        setattr(order, field, value)

    db.commit()
    db.refresh(order)
    return order


def delete_order_by_id(db: Session, order_id: int):
    order = get_order_by_id(db, order_id)
    if order:
        db.delete(order)
        db.commit()
    return 