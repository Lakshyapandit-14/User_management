from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.common.utils import create_access_token, verify_password
from app.core.config import settings
from app.core.common.exceptions import NotFoundException, InvalidCredentialsException
from app.services.users.models import User
from app.services.auth.jwt import schemas
from fastapi import Depends, Header, HTTPException

#SECRET_KEY = "your-secret-key"
#ALGORITHM = "HS256"
#ACCESS_TOKEN_EXPIRE_MINUTES = 30    

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

class AuthService:

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise NotFoundException("User not found")
        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException("Invalid password")
        return user

    @staticmethod
    def create_user_token(user: User):
        token_data = {"sub": user.username}
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(data=token_data, expires_delta=access_token_expires)
        return token

    @staticmethod
    def login_user(db: Session, login_data: schemas.TokenRequest):
        user = AuthService.authenticate_user(db, login_data.username, login_data.password)
        token = AuthService.create_user_token(user)
        return schemas.TokenResponse(access_token=token)

    @staticmethod
    def decode_access_token(token: str):
        """
        Decode a JWT token and return its payload.
        Raises InvalidCredentialsException if invalid or expired.      #3rd
        """
        if not token or not isinstance(token, str):
            raise InvalidCredentialsException("No JWT token provided for decoding.")
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise InvalidCredentialsException("Invalid or expired token")

    @staticmethod
    def verify_token(token: str, db: Session):
        """
        Verify a JWT token, return a message and decoded payload.          #2nd 
        Raises InvalidCredentialsException if invalid.
        """
        payload = AuthService.decode_access_token(token)
        return {"message": "Token is valid", "user": payload}

    @staticmethod
    def verify_token_from_header(authorization: str, db: Session):
        """
        Extract token from Authorization header and verify it.
        Raises HTTPException(401) for missing/invalid header.                  #1st 
        """
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid token header")

        # Split and strip to ensure no extra spaces break the logic
        parts = authorization.split(" ")
        if len(parts) != 2 or not parts[1]:
            raise HTTPException(status_code=401, detail="Invalid token format")

        token = parts[1].strip()
        return AuthService.verify_token(token, db)

    @staticmethod
    def verify_jwt_from_header_or_token(token_or_authorization: str, db: Session):
        """
        Accepts either a JWT token directly or an Authorization header value.
        Extracts and verifies the token, returns decoded payload.
        Raises HTTPException(401) or InvalidCredentialsException if missing/invalid.
        """
        # Detect if input is an Authorization header
        token = token_or_authorization
        if token_or_authorization.startswith("Bearer "):
            parts = token_or_authorization.split(" ")
            if len(parts) != 2 or not parts[1].strip():
                raise HTTPException(status_code=401, detail="Invalid token format")
            token = parts[1].strip()

        if not token or not isinstance(token, str):
            raise InvalidCredentialsException("No JWT token provided for decoding.")

        # Decode and verify token
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return {"message": "Token is valid", "user": payload}
        except JWTError:
            raise InvalidCredentialsException("Invalid or expired token")
