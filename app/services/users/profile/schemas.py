from pydantic import BaseModel, HttpUrl
from typing import Optional

class ProfileBase(BaseModel):
    bio: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True