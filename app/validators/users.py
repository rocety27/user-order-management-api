from pydantic import BaseModel, EmailStr, constr, Field
from typing import Annotated, Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: Annotated[str, constr(min_length=3, max_length=255)]
    email: EmailStr
    password: Annotated[str, constr(min_length=6, max_length=255)]
    role: str = "customer"

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=255)
    email: Optional[EmailStr] = None

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True