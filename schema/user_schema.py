from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    name: str
    email: EmailStr
    username: str
    password: str
    role: Optional[str] = "user"