from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ---------- Base Schema ----------
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


# ---------- Create Schema ----------
class UserCreate(UserBase):
    password: str


# ---------- Response Schema ----------
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Login Schema ----------
class UserLogin(BaseModel):
    username: str
    password: str


# ---------- Update Schema ----------
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
