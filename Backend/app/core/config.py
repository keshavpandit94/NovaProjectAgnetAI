# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    
    # Database Settings
    MONGO_URI: str
    GEMINI_API_KEY: str
    
    # NEW: JWT Settings - MUST BE CHANGED IN .env
    SECRET_KEY: str = "YOUR_SUPER_SECRET_JWT_KEY_HERE_CHANGE_ME"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 1 day
    
    # NEW: Cloudinary Settings
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

settings = Settings()