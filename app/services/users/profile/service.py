from sqlalchemy.orm import Session
from app.services.users.profile import models, schemas

def create_profile(db: Session, user_id: int, profile_data: schemas.ProfileCreate):
    profile = models.UserProfile(user_id=user_id, **profile_data.dict())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

def get_profile(db: Session, user_id: int):
    return db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()

def update_profile(db: Session, user_id: int, update_data: schemas.ProfileUpdate):
    profile = get_profile(db, user_id)
    if not profile:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile
