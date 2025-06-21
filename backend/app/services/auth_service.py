from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from fastapi import HTTPException, status
from app.models import User
from app.schemas import UserCreate, Token
from app.core.security import verify_password, get_password_hash, create_tokens

class AuthService:
    @staticmethod
    async def register(db: AsyncSession, user_data: UserCreate) -> User:
        """Register a new user"""
        # Check if username or email already exists
        result = await db.execute(
            select(User).where(
                or_(
                    User.username == user_data.username,
                    User.email == user_data.email
                )
            )
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            if existing_user.username == user_data.username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already registered"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        return new_user
    
    @staticmethod
    async def authenticate(
        db: AsyncSession, 
        username: str, 
        password: str
    ) -> Optional[User]:
        """Authenticate a user by username/email and password"""
        # Allow login with either username or email
        result = await db.execute(
            select(User).where(
                or_(
                    User.username == username,
                    User.email == username
                )
            )
        )
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        
        if not verify_password(password, user.password_hash):
            return None
        
        # Update last login
        user.last_login_at = datetime.now()
        await db.commit()
        
        return user
    
    @staticmethod
    async def create_tokens_for_user(user: User) -> Token:
        """Create access and refresh tokens for a user"""
        token_dict = create_tokens(user.id, user.username)
        return Token(**token_dict)