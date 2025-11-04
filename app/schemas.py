
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str
    display_name: Optional[str] = None

    model_config = {"from_attributes": True}

class UserOut(BaseModel):
    id: int
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    display_name: Optional[str] = None

    model_config = {"from_attributes": True}
