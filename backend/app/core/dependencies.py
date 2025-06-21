from typing import Optional, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError
from app.database import get_db
from app.models import User
from app.schemas import TokenData
from app.core.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    """Get the current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verify token
    payload = verify_token(token, token_type="access")
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Get user from database
    result = await db.execute(
        select(User).where(User.id == int(user_id))
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """Ensure the current user is active"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

# Role-based dependencies
async def get_admin_user(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """Ensure the current user is an admin"""
    if current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

async def get_instructor_user(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """Ensure the current user is at least an instructor"""
    if current_user.role.value not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

# Optional authentication
async def get_current_user_optional(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[Optional[str], Depends(oauth2_scheme)]
) -> Optional[User]:
    """Get the current user if authenticated, None otherwise"""
    if not token:
        return None
    
    try:
        return await get_current_user(db, token)
    except HTTPException:
        return None