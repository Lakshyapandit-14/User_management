from pydantic import BaseModel
from typing import Optional


# ---------- Login Request Schema ----------
class TokenRequest(BaseModel):
    username: str
    password: str


# ---------- Token Response Schema ----------
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Token Payload (Data inside JWT) ----------
class TokenPayload(BaseModel):
    sub: Optional[str] = None  # usually username or user ID
    exp: Optional[int] = None  # expiration time

class SignupResponse(BaseModel):
    username: str
    password: str
