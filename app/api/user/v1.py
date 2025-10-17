from fastapi import APIRouter
from app.services.users.routes import router as user_routes

# Versioned User Router
router = APIRouter()

# Include user-related routes
router.include_router(user_routes, prefix="", tags=["Users"])
