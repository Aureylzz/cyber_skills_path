from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from app.models import SubTheme, Category
from app.schemas import SubThemeCreate, SubThemeUpdate

class SubThemeService:
    @staticmethod
    async def create_sub_theme(
        db: AsyncSession,
        sub_theme_data: SubThemeCreate
    ) -> SubTheme:
        """Create a new sub-theme"""
        # Verify category exists
        category_result = await db.execute(
            select(Category).where(Category.id == sub_theme_data.category_id)
        )
        if not category_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        # Check if sub-theme name already exists in this category
        result = await db.execute(
            select(SubTheme).where(
                and_(
                    SubTheme.category_id == sub_theme_data.category_id,
                    func.lower(SubTheme.name) == sub_theme_data.name.lower()
                )
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sub-theme with this name already exists in this category"
            )
        
        sub_theme = SubTheme(**sub_theme_data.model_dump())
        db.add(sub_theme)
        await db.commit()
        await db.refresh(sub_theme)
        return sub_theme
    
    @staticmethod
    async def get_sub_themes(
        db: AsyncSession,
        category_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
        include_category: bool = False
    ) -> List[SubTheme]:
        """Get sub-themes, optionally filtered by category"""
        query = select(SubTheme).offset(skip).limit(limit)
        
        if category_id:
            query = query.where(SubTheme.category_id == category_id)
        
        if include_category:
            query = query.options(selectinload(SubTheme.category))
        
        query = query.order_by(SubTheme.display_order)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_sub_theme(
        db: AsyncSession,
        sub_theme_id: int,
        include_category: bool = False
    ) -> Optional[SubTheme]:
        """Get a single sub-theme by ID"""
        query = select(SubTheme).where(SubTheme.id == sub_theme_id)
        
        if include_category:
            query = query.options(selectinload(SubTheme.category))
        
        result = await db.execute(query)
        sub_theme = result.scalar_one_or_none()
        
        if not sub_theme:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sub-theme not found"
            )
        
        return sub_theme
    
    @staticmethod
    async def update_sub_theme(
        db: AsyncSession,
        sub_theme_id: int,
        sub_theme_data: SubThemeUpdate
    ) -> SubTheme:
        """Update a sub-theme"""
        sub_theme = await SubThemeService.get_sub_theme(db, sub_theme_id)
        
        update_data = sub_theme_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(sub_theme, field, value)
        
        await db.commit()
        await db.refresh(sub_theme)
        return sub_theme
    
    @staticmethod
    async def delete_sub_theme(
        db: AsyncSession,
        sub_theme_id: int
    ) -> dict:
        """Delete a sub-theme (cascades to questions)"""
        sub_theme = await SubThemeService.get_sub_theme(db, sub_theme_id)
        
        await db.delete(sub_theme)
        await db.commit()
        
        return {"message": f"Sub-theme '{sub_theme.name}' deleted successfully"}
