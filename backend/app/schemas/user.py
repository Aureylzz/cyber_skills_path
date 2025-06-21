from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseSchema, TimestampSchema
from app.models.enums import UserRole

# Request schemas
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)

# Response schemas
class UserBase(BaseSchema):
    id: int
    username: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    role: UserRole
    is_active: bool

class UserResponse(UserBase, TimestampSchema):
    last_login_at: Optional[datetime]
    
    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

class UserInDB(UserResponse):
    password_hash: str

# Token schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None