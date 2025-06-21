from typing import List, Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import (
    CategoryCreate, CategoryUpdate, CategoryResponse, 
    CategoryWithSubThemes, PaginationParams
)
from app.services.category_service import CategoryService
from app.core.dependencies import get_admin_user, get_current_user
from app.models import User

router = APIRouter()

@router.post("/", response_model=CategoryResponse)
async def create_category(
    category_data: CategoryCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin_user: Annotated[User, Depends(get_admin_user)]
):
    """Create a new category (Admin only)"""
    return await CategoryService.create_category(db, category_data)

@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    include_sub_themes: bool = Query(False)
):
    """Get all categories (Public)"""
    return await CategoryService.get_categories(
        db, skip, limit, include_sub_themes
    )

@router.get("/{category_id}", response_model=CategoryWithSubThemes)
async def get_category(
    category_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get a single category with sub-themes (Public)"""
    return await CategoryService.get_category(
        db, category_id, include_sub_themes=True
    )

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin_user: Annotated[User, Depends(get_admin_user)]
):
    """Update a category (Admin only)"""
    return await CategoryService.update_category(
        db, category_id, category_data
    )

@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin_user: Annotated[User, Depends(get_admin_user)]
):
    """Delete a category (Admin only)"""
    return await CategoryService.delete_category(db, category_id)
