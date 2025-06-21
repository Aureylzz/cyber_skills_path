from typing import List, Annotated, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import (
    SubThemeCreate, SubThemeUpdate, SubThemeResponse,
    SubThemeWithCategory
)
from app.services.sub_theme_service import SubThemeService
from app.core.dependencies import get_admin_user, get_current_user
from app.models import User

router = APIRouter()

@router.post("/", response_model=SubThemeResponse)
async def create_sub_theme(
    sub_theme_data: SubThemeCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin_user: Annotated[User, Depends(get_admin_user)]
):
    """Create a new sub-theme (Admin only)"""
    return await SubThemeService.create_sub_theme(db, sub_theme_data)

@router.get("/", response_model=List[SubThemeResponse])
async def get_sub_themes(
    db: Annotated[AsyncSession, Depends(get_db)],
    category_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    include_category: bool = Query(False)
):
    """Get sub-themes, optionally filtered by category (Public)"""
    return await SubThemeService.get_sub_themes(
        db, category_id, skip, limit, include_category
    )

@router.get("/{sub_theme_id}", response_model=SubThemeWithCategory)
async def get_sub_theme(
    sub_theme_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get a single sub-theme with category info (Public)"""
    return await SubThemeService.get_sub_theme(
        db, sub_theme_id, include_category=True
    )

@router.put("/{sub_theme_id}", response_model=SubThemeResponse)
async def update_sub_theme(
    sub_theme_id: int,
    sub_theme_data: SubThemeUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin_user: Annotated[User, Depends(get_admin_user)]
):
    """Update a sub-theme (Admin only)"""
    return await SubThemeService.update_sub_theme(
        db, sub_theme_id, sub_theme_data
    )

@router.delete("/{sub_theme_id}")
async def delete_sub_theme(
    sub_theme_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin_user: Annotated[User, Depends(get_admin_user)]
):
    """Delete a sub-theme (Admin only)"""
    return await SubThemeService.delete_sub_theme(db, sub_theme_id)
