from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db.crud.orders import (
    create_order as create_order_db,
    get_all_orders,
    get_orders_by_user_id,
    get_order_by_id,
    # update_order_db,
    # delete_order_by_id
)
from app.validators.orders import OrderCreate, OrderUpdate

def create_order_service(db: Session, user_id: int, order_in: OrderCreate):
    return create_order_db(
        db=db,
        user_id=user_id,
        total_amount=order_in.total_amount,
        status=order_in.status
    )

def list_orders_service(db: Session):
    return get_all_orders(db)


def list_my_orders_service(db: Session, user_id: int):
    return get_orders_by_user_id(db, user_id)


def get_order_service(db: Session, order_id: int):
    return get_order_by_id(db, order_id)


# def update_order_service(db: Session, order_id: int, order_update: OrderUpdate, current_user_id: int, is_admin: bool):
#     order = get_order_by_id(db, order_id)
#     if not order:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
#     if not is_admin and order.user_id != current_user_id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
#     return update_order_db(db, order_id, order_update)


# def delete_order_service(db: Session, order_id: int, current_user_id: int, is_admin: bool):
#     order = get_order_by_id(db, order_id)
#     if not order:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
#     if not is_admin and order.user_id != current_user_id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
#     delete_order_by_id(db, order_id)


# def list_orders_by_user_id_service(db: Session, user_id: int):
#     return get_orders_by_user_id(db, user_id)
