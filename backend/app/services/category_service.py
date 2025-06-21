from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from app.models import Category, SubTheme
from app.schemas import CategoryCreate, CategoryUpdate

class CategoryService:
    @staticmethod
    async def create_category(
        db: AsyncSession, 
        category_data: CategoryCreate
    ) -> Category:
        """Create a new category"""
        # Check if category name already exists
        result = await db.execute(
            select(Category).where(
                func.lower(Category.name) == category_data.name.lower()
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists"
            )
        
        category = Category(**category_data.model_dump())
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category
    
    @staticmethod
    async def get_categories(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        include_sub_themes: bool = False
    ) -> List[Category]:
        """Get all categories"""
        query = select(Category).offset(skip).limit(limit).order_by(Category.display_order)
        
        if include_sub_themes:
            query = query.options(selectinload(Category.sub_themes))
        
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_category(
        db: AsyncSession,
        category_id: int,
        include_sub_themes: bool = False
    ) -> Optional[Category]:
        """Get a single category by ID"""
        query = select(Category).where(Category.id == category_id)
        
        if include_sub_themes:
            query = query.options(selectinload(Category.sub_themes))
        
        result = await db.execute(query)
        category = result.scalar_one_or_none()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        return category
    
    @staticmethod
    async def update_category(
        db: AsyncSession,
        category_id: int,
        category_data: CategoryUpdate
    ) -> Category:
        """Update a category"""
        category = await CategoryService.get_category(db, category_id)
        
        # Update only provided fields
        update_data = category_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)
        
        await db.commit()
        await db.refresh(category)
        return category
    
    @staticmethod
    async def delete_category(
        db: AsyncSession,
        category_id: int
    ) -> dict:
        """Delete a category (cascades to sub-themes and questions)"""
        category = await CategoryService.get_category(db, category_id)
        
        await db.delete(category)
        await db.commit()
        
        return {"message": f"Category '{category.name}' deleted successfully"}
    
    @staticmethod
    async def get_category_count(db: AsyncSession) -> int:
        """Get total number of categories"""
        result = await db.execute(select(func.count(Category.id)))
        return result.scalar()
