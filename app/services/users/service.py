from sqlalchemy.orm import Session
from app.core.common.utils import hash_password, verify_password
from app.services.users import models, schemas
from app.core.common.exceptions import NotFoundException

class UserService:

    @staticmethod
    def create_user(db: Session, user_data: schemas.UserCreate):
        existing_user = db.query(models.User).filter(
            (models.User.username == user_data.username) | (models.User.email == user_data.email)
        ).first()
        if existing_user:
            raise NotFoundException("User with this username or email already exists")

        hashed_pwd = hash_password(user_data.password)
        new_user = models.User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_pwd,
            full_name=user_data.full_name
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user:
            raise NotFoundException("User not found")
        return user

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user:
            raise NotFoundException("User not found")
        if not verify_password(password, user.hashed_password):
            raise NotFoundException("Invalid username or password")
        return user

    @staticmethod
    def update_user(db: Session, user_id: int, update_data: schemas.UserUpdate):
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise NotFoundException("User not found")

        if update_data.full_name is not None:
            user.full_name = update_data.full_name
        if update_data.email is not None:
            user.email = update_data.email
        if update_data.password is not None:
            user.hashed_password = hash_password(update_data.password)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_all_users(db: Session):
        users = db.query(models.User).all()
        if not users:
            raise NotFoundException("No users found")
        return users

    @staticmethod
    def get_user(db: Session, user_id: int):
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise NotFoundException("User not found")
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise NotFoundException("User not found")
        db.delete(user)
        db.commit()
        return {"detail": "User deleted successfully"}