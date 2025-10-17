from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.connections.database import get_db

# User service & schemas
from app.services.users import service as user_service, schemas as user_schemas

# Profile service & schemas
from app.services.users.profile import service as profile_service, schemas as profile_schemas
from app.services.users.service import UserService
from app.services.users.profile.service import ProfileService

router = APIRouter(prefix="/users", tags=["Users"])

# --- User CRUD Endpoints ---
@router.post("/", response_model=user_schemas.UserResponse)
def create_user(user_data: user_schemas.UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db, user_data)

@router.get("/", response_model=List[user_schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return UserService.get_all_users(db)

@router.get("/{user_id}", response_model=user_schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return UserService.get_user(db, user_id)

@router.put("/{user_id}", response_model=user_schemas.UserResponse)
def update_user(user_id: int, user_data: user_schemas.UserUpdate, db: Session = Depends(get_db)):
    return UserService.update_user(db, user_id, user_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return UserService.delete_user(db, user_id)

# --- Profile Endpoints (nested under /users/profile) ---
profile_router = APIRouter(prefix="/profile", tags=["Profile"])

@profile_router.post("/{user_id}/profile", response_model=profile_schemas.ProfileResponse)
def create_user_profile(user_id: int, data: profile_schemas.ProfileCreate, db: Session = Depends(get_db)):
    return ProfileService.create_profile(db, user_id, data)

@profile_router.get("/{user_id}", response_model=profile_schemas.ProfileResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    return ProfileService.get_profile(db, user_id)

@profile_router.put("/{user_id}", response_model=profile_schemas.ProfileResponse)
def update_user_profile(user_id: int, data: profile_schemas.ProfileUpdate, db: Session = Depends(get_db)):
    return ProfileService.update_profile(db, user_id, data)

# Attach profile routes under /users/profile
router.include_router(profile_router)