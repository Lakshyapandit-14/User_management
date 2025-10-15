from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.connections.database import get_db
from app.services.users.profile import schemas, service

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.post("/{user_id}", response_model=schemas.ProfileResponse)
def create_user_profile(user_id: int, data: schemas.ProfileCreate, db: Session = Depends(get_db)):
    return service.create_profile(db, user_id, data)

@router.get("/{user_id}", response_model=schemas.ProfileResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    profile = service.get_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile

@router.put("/{user_id}", response_model=schemas.ProfileResponse)
def update_user_profile(user_id: int, data: schemas.ProfileUpdate, db: Session = Depends(get_db)):
    profile = service.update_profile(db, user_id, data)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile
