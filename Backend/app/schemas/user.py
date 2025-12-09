# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# --- Authentication Schemas ---

class UserCreate(BaseModel):
    """Input schema for user registration."""
    email: EmailStr
    username: str # NEW
    name: Optional[str] = None # NEW
    dob: Optional[date] = None # NEW (Requires 'date' type)
    password: str

class UserLogin(BaseModel):
    """Input schema for user login (username is used for email)."""
    username: str 
    password: str

class Token(BaseModel):
    """Output schema for a successful login."""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Data stored inside the JWT token (payload)."""
    user_id: Optional[str] = None