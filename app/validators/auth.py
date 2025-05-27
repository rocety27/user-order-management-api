from pydantic import BaseModel
from typing import List

class TokenData(BaseModel):
    user_id: int
    role: str
    permissions: List[str]
