from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    password: str
    display_name: Optional[str] = None

class UserOut(BaseModel):
    id: int
    email: Optional[str] = None
    phone: Optional[str] = None
    display_name: Optional[str] = None

    class Config:
        orm_mode = True
