from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List

from sqlalchemy.orm import Session
from app.db.session import get_db

from app.validators.orders import OrderCreate, OrderUpdate, OrderOut
from app.validators.auth import TokenData

from app.services.orders import (
    create_order_service,
    list_orders_service,
    # get_order_service,
    # update_order_service,
    # delete_order_service,
    # list_orders_by_user_service,
    # list_my_orders_service,
)

from app.utils.jwt import (
    get_current_user,
    permission_required,
)

router = APIRouter()

@router.post("/", summary="Create a new order", response_model=OrderOut)
def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(permission_required("can_create_order")),
):
    try:
        print(f"Creating order for user: {current_user.user_id} with data: {order_in}")
        order = create_order_service(db, current_user.user_id, order_in)
        print(f"Order created successfully: {order}")
        return order
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")
    

@router.get("/", summary="List all orders", response_model=List[OrderOut])
def list_orders(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(permission_required("can_list_all_orders")),
):
    try:
        return list_orders_service(db)
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")

# @router.get("/{order_id}", summary="Get order by ID", response_model=OrderOut)
# def get_order(
#     order_id: int,
#     db: Session = Depends(get_db),
#     current_user: TokenData = Depends(get_current_user),
# ):
#     try:
#         order = get_order_service(db, order_id)

#         if "can_get_order" not in current_user.permissions and order.user_id != current_user.user_id:
#             raise HTTPException(status_code=403, detail="Access denied.")
        
#         return order
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         raise HTTPException(status_code=500, detail="Unexpected error occurred.")

# # --- Update Order ---
# @router.put("/{order_id}", summary="Update order by ID", response_model=OrderOut)
# def update_order(
#     order_id: int,
#     order_update: OrderUpdate,
#     db: Session = Depends(get_db),
#     current_user: TokenData = Depends(get_current_user),
# ):
#     try:
#         order = get_order_service(db, order_id)

#         if "can_update_order" not in current_user.permissions and order.user_id != current_user.user_id:
#             raise HTTPException(status_code=403, detail="Access denied.")

#         updated_order = update_order_service(db, order_id, order_update)
#         return updated_order
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         raise HTTPException(status_code=500, detail="Unexpected error occurred.")

# # --- Delete Order ---
# @router.delete("/{order_id}", summary="Delete order by ID", status_code=200)
# def delete_order(
#     order_id: int,
#     db: Session = Depends(get_db),
#     current_user: TokenData = Depends(get_current_user),
# ):
#     try:
#         order = get_order_service(db, order_id)

#         if "can_delete_order" not in current_user.permissions and order.user_id != current_user.user_id:
#             raise HTTPException(status_code=403, detail="Access denied.")

#         delete_order_service(db, order_id)
#         return JSONResponse(content={"message": f"Order {order_id} deleted."})
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         raise HTTPException(status_code=500, detail="Unexpected error occurred.")


# # --- List Orders by Specific User ---
# @router.get("/users/{user_id}/orders", summary="List orders by user", response_model=List[OrderOut])
# def list_user_orders(
#     user_id: int,
#     db: Session = Depends(get_db),
#     current_user: TokenData = Depends(permission_required("can_list_user_orders")),
# ):
#     try:
#         return list_orders_by_user_service(db, user_id)
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         raise HTTPException(status_code=500, detail="Unexpected error occurred.")

# # --- List Orders of Logged-In Customer ---
# @router.get("/me", summary="List own orders", response_model=List[OrderOut])
# def list_my_orders(
#     db: Session = Depends(get_db),
#     current_user: TokenData = Depends(get_current_user),
# ):
#     try:
#         return list_my_orders_service(db, current_user.user_id)
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         raise HTTPException(status_code=500, detail="Unexpected error occurred.")
