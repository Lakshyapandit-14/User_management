from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from app.services.auth.jwt import schemas, service

router = APIRouter()


# ---------- Login Endpoint ----------
@router.post("/login", response_model=schemas.TokenResponse, status_code=status.HTTP_200_OK)
def login(login_data: schemas.TokenRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT access token"""
    return service.login_user(db, login_data)


# ---------- Protected Example (Optional) ----------
@router.get("/verify-token")
def verify_token_example():
    """Placeholder for verifying tokens (can be extended later)"""
    return {"message": "Token verification endpoint — to be implemented"}
