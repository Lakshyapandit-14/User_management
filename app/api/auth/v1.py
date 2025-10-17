from fastapi import APIRouter
from app.services.auth.jwt.routes import router as auth_routes

# Versioned Auth Router
router = APIRouter()

# Include all authentication-related routes (login, logout, refresh)
router.include_router(auth_routes, prefix="", tags=["Auth"])
