from datetime import timedelta
from sqlalchemy.orm import Session
from app.core.common.utils import create_access_token, verify_password
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.common.exceptions import InvalidCredentialsException, UserNotFoundException
from app.services.users.models import User
from app.services.auth.jwt import schemas


# ---------- Authenticate User ----------
def authenticate_user(db: Session, username: str, password: str):
    """Verify user credentials"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise UserNotFoundException("User not found")

    if not verify_password(password, user.hashed_password):
        raise InvalidCredentialsException("Invalid password")

    return user


# ---------- Generate JWT Token ----------
def create_user_token(user: User):
    """Generate JWT token for authenticated user"""
    token_data = {"sub": user.username}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data=token_data, expires_delta=access_token_expires)
    return token


# ---------- Login Logic ----------
def login_user(db: Session, login_data: schemas.TokenRequest):
    """Handle login and return JWT"""
    user = authenticate_user(db, login_data.username, login_data.password)
    token = create_user_token(user)
    return schemas.TokenResponse(access_token=token)
