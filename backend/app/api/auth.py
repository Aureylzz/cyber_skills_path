from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import UserCreate, UserResponse, Token
from app.services.auth_service import AuthService
from app.core.dependencies import get_current_user
from app.core.security import verify_token, create_tokens
from app.models import User

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Register a new user"""
    user = await AuthService.register(db, user_data)
    return user

@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Login with username/email and password"""
    user = await AuthService.authenticate(
        db, 
        form_data.username, 
        form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return await AuthService.create_tokens_for_user(user)

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Refresh access token using refresh token"""
    # Verify refresh token
    payload = verify_token(refresh_token, token_type="refresh")
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    username = payload.get("username")
    
    if not user_id or not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    # Create new tokens
    token_dict = create_tokens(int(user_id), username)
    return Token(**token_dict)

@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Get current user info"""
    return current_user

@router.post("/logout")
async def logout():
    """Logout (client should discard tokens)"""
    # In a more complex system, you might want to:
    # - Add the token to a blacklist
    # - Clear server-side sessions
    # - Log the logout event
    return {"message": "Successfully logged out"}