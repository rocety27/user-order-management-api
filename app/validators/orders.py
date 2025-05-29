from typing import Annotated, Optional
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime


class OrderCreate(BaseModel):
    total_amount: Annotated[Decimal, Field(gt=0, decimal_places=2)]
    status: Optional[Annotated[str, Field(max_length=50)]] = "pending"


class OrderUpdate(BaseModel):
    total_amount: Optional[Annotated[Decimal, Field(gt=0, decimal_places=2)]] = None
    status: Optional[Annotated[str, Field(max_length=50)]] = None


class OrderOut(BaseModel):
    id: int
    user_id: int
    order_date: datetime
    total_amount: Decimal
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
