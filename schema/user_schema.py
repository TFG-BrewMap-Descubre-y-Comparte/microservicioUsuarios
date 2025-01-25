from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    name: str
    email: EmailStr
    username: str
    password: str
    role: Optional[str] = "user"

class DataUser(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id_user: int
    username: str
    name: str
    email: str
    role: str

class ErrorResponse(BaseModel):
    error: str

class MessageResponse(BaseModel):
    message: str