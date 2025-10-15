import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings  # ✅ Correct import for Pydantic v2

# Load environment variables
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

class Settings(BaseSettings):
    APP_NAME: str = "User Management Microservice"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "A FastAPI-based microservice for user authentication and management."
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./user_management.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

settings = Settings()

# If you want to support both `settings.ACCESS_TOKEN_EXPIRE_MINUTES` and direct import
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES