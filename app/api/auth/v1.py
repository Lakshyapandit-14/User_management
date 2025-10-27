from fastapi import APIRouter, Depends, status, Header
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from app.services.auth.jwt import schemas
from app.services.auth.jwt.service import AuthService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer()

# ---------- Login Endpoint ----------
@router.post("/login", response_model=schemas.TokenResponse, status_code=status.HTTP_200_OK)
def login(login_data: schemas.TokenRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT access token"""
    return AuthService.login_user(db, login_data)



from fastapi import Depends, Header
# ---------- Verify Token Endpoint ----------
@router.get("/verify-token")
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security),db: Session = Depends(get_db)):
    """
    Verify the JWT token from the Authorization header.
    Expected format: Authorization: Bearer <token>
    """
    token = credentials.credentials # this is only the token

    return AuthService.verify_token(token, db) #→ expects only the token. Use it if you’re using HTTPBearer() dependency.
    #return AuthService.verify_jwt_from_header_or_token(authorization, db)
    #return AuthService.verify_token_from_header(token, db)  → expects "Bearer <token>". Use it if you take the raw header.

#If you want to support both direct tokens and header values, 
# use verify_jwt_from_header_or_token.

# ---------- Signup ----------

from app.services.users.schemas import UserCreate

# SignupResponse is provided by app.services.auth.jwt.schemas which is already imported as `schemas`
@router.post("/signup", response_model=schemas.SignupResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    return AuthService.signup_user(db, user_data)