from sqlalchemy.orm import Session
from app.services.users.profile import models, schemas
from app.core.common.exceptions import NotFoundException, AlreadyExistsException
from pydantic import HttpUrl
#new
from app.services.users.models import User
from app.services.users.profile import models
#
from app.services.users.models import User
from app.services.users.profile.models import UserProfile
from app.core.common import exceptions


class ProfileService:

    @staticmethod
    def create_profile(db: Session, user_id: int, profile_data: schemas.ProfileCreate):
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException("User not found")

        # Check if profile already exists
        existing_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if existing_profile:
            raise AlreadyExistsException("Profile already exists for this user")

        # Convert Pydantic HttpUrl to str for avatar_url
        data = profile_data.dict()
        if data.get("avatar_url") is not None:
            data["avatar_url"] = str(data["avatar_url"])

        profile = models.UserProfile(user_id=user_id, **data)
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile


    @staticmethod
    def get_profile(db: Session, user_id: int):
        profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
        if not profile:
            raise NotFoundException("Profile not found")
        return profile

    @staticmethod
    def update_profile(db: Session, user_id: int, data: schemas.ProfileUpdate):
        profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
        if not profile:
            raise NotFoundException("Profile not found")
        # Update logic
        update_data = data.dict(exclude_unset=True)
        update_data.pop("user_id", None)
        for key, value in update_data.items():
            if isinstance(value, HttpUrl):
                value = str(value)
            setattr(profile, key, value)
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def delete_profile(db: Session, user_id: int):
        profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
        if not profile:
            raise NotFoundException("Profile not found")
        db.delete(profile)
        db.commit()
        return True