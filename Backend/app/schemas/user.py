from pydantic import BaseModel, EmailStr
from typing import Optional, List # Imported List
from datetime import date

# Import the HistoryItem schema from your chat file
# NOTE: You must ensure this path is correct in your project structure (e.g., app.schemas.chat)
from app.schemas.chat import HistoryItem 

# --- Authentication Schemas ---

class UserCreate(BaseModel):
    """Input schema for user registration."""
    email: EmailStr
    username: str
    name: Optional[str] = None
    dob: Optional[date] = None
    password: str

class UserLogin(BaseModel):
    """Input schema for user login (username is used for email)."""
    username: str 
    password: str

class Token(BaseModel):
    """
    Output schema for a successful login.
    UPDATED: Includes a list of past chat sessions for frontend rendering.
    """
    access_token: str
    token_type: str = "bearer"
    # NEW FIELD: History items retrieved on login
    chat_history: List[HistoryItem] = [] 

class TokenData(BaseModel):
    """Data stored inside the JWT token (payload)."""
    user_id: Optional[str] = None