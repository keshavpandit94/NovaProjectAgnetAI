from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.database.models import User
from app.schemas.user import UserCreate, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings # Ensure this is imported for settings access
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=Token)
async def signup(user_data: UserCreate):
    """Register a new user and return an access token."""
    
    if User.objects(email=user_data.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if User.objects(username=user_data.username).first(): # Check unique username
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    # Hash Password and Create User
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email, 
        username=user_data.username, # NEW
        name=user_data.name, # NEW
        dob=user_data.dob, # NEW
        hashed_password=hashed_password
    )
    user.save()
    
    # 3. Create Access Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user with email (username) and password."""
    
    # 1. Find User by email (username is the email field in the OAuth2 form)
    user = User.objects(email=form_data.username).first()
    
    # 2. Verify Credentials
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Create Access Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}