from fastapi import APIRouter, Depends, status, Header
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from app.services.auth.jwt import schemas
from app.services.auth.jwt.service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

# ---------- Login Endpoint ----------
@router.post("/login", response_model=schemas.TokenResponse, status_code=status.HTTP_200_OK)
def login(login_data: schemas.TokenRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT access token"""
    return AuthService.login_user(db, login_data)



from fastapi import Depends, Header
# ---------- Verify Token Endpoint ----------
@router.get("/verify-token")
def verify_token(db: Session = Depends(get_db), authorization: str = Header(None)):
    """
    Verify the JWT token from the Authorization header.
    Expected format: Authorization: Bearer <token>
    """
    return AuthService.verify_token(authorization, db)
    #return AuthService.verify_jwt_from_header_or_token(authorization, db)
