from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, exceptions
from pwdlib import PasswordHash
from fastapi import HTTPException, status, Depends
# IMPORTS UPDATED: Using HTTPBearer for optional token retrieval
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials 

from app.core.config import settings
from app.database.models import User
from app.schemas.user import TokenData

# Initialize Password Hashing (Argon2)
password_context = PasswordHash.recommended()

# Dependency for Login Endpoint (Uses standard OAuth2PasswordBearer)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# NEW: Dependency for Optional Token Retrieval (Does not raise 401 on missing header)
bearer_scheme = HTTPBearer(auto_error=False) 

# --- Password Hashing Functions ---

def get_password_hash(password: str) -> str:
    """Hashes a plain text password."""
    return password_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against a hash."""
    try:
        return password_context.verify(plain_password, hashed_password)
    except exceptions.InvalidTokenError:
        return False

# --- JWT Token Functions ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a JWT token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "sub": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# --- Dependency to Get Current User ID (The Core Logic - UPDATED) ---

async def get_current_user_id(
    # Use HTTPBearer, which will pass None if the header is missing
    security_info: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)
) -> Optional[str]:
    """
    Extracts and validates the JWT token.
    Returns user_id (str) if logged in, or None if anonymous/token is invalid.
    """
    
    # Extract the token string safely
    token = security_info.credentials if security_info else None
    
    if token is None:
        # If no token is found in the header, treat as Anonymous user
        return None
    
    try:
        # Decode the token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # Get the user ID from the payload
        user_id: str = payload.get("user_id")
        if user_id is None:
            # Token is valid but user_id is missing: Treat as anonymous
            return None
        
        # Verify user exists in DB (essential for security)
        user = User.objects(id=user_id).first()
        if user is None:
            # User deleted since token was issued: Treat as anonymous
            return None
            
        return user_id

    except exceptions.JWTError:
        # Token is expired, invalid signature, or malformed: Treat as anonymous
        return None
    except Exception:
        # Catch any other database or decoding error: Treat as anonymous
        return None