from pydantic import BaseModel, EmailStr, constr
from typing import Annotated

class UserCreate(BaseModel):
    username: Annotated[str, constr(min_length=3, max_length=255)]
    email: EmailStr
    password: Annotated[str, constr(min_length=6, max_length=255)]
    role: str = "customer"

from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
