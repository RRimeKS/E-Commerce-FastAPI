from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    firstName: str = Field(min_length=3, max_length=64)
    lastName: str = Field(min_length=2, max_length=64)
    userName: str = Field(min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)

class UserLogin(BaseModel):
    identifier: str
    password: str

class UserResponse(BaseModel):
    id: int
    userName: str
    role: str
    createdAt: datetime

    class Config():
        from_attributes: True