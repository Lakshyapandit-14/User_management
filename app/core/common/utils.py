from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from app.core.config import settings
from typing import Optional

# Load values from settings
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Password hashing context using Argon2 (no need for truncation)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# --- Password Utilities ---
def hash_password(password: str) -> str:
    """Hash plain text password using Argon2."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that a plain password matches the hashed version using Argon2."""
    return pwd_context.verify(plain_password, hashed_password)

# --- JWT Token Utilities ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """Decode a JWT token and return the payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
    from passlib.context import CryptContext

# Create a password hashing context
# for signup 
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.
    Returns the hashed password as a string.
    """
    return pwd_context.hash(password)