from pydantic import BaseModel, EmailStr
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserRegister(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str
    display_name: str = "Anonymous"

class UserLogin(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str

class ProfileIn(BaseModel):
    age: int = 18
    location: str = ""
    bio: str = ""
    intentions: List[str] = []
    trust: float = 3.0
    photo_url: str = ""

class PactIn(BaseModel):
    partner_id: Optional[int] = None
    when: str = ""
    where: str = ""
    note: str = ""

class GiftIn(BaseModel):
    pact_code: str
    recipient_id: Optional[int] = None
    amount: str
    method: str = "Wallet"

class StoryIn(BaseModel):
    pact_code: str = ""
    category: str = "Chaotic"
    location: str = ""
    text: str
    anon: bool = True
    ratings_csv: str = "4,4,4"

class ReactIn(BaseModel):
    kind: str
