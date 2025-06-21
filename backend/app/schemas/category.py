from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.base import BaseSchema, TimestampSchema

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    display_order: int = Field(..., ge=0)

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    display_order: Optional[int] = Field(None, ge=0)

class CategoryBase(BaseSchema):
    id: int
    name: str
    display_order: int

class CategoryResponse(CategoryBase, TimestampSchema):
    pass

# Sub-theme schemas
class SubThemeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    display_order: int = Field(..., ge=0)
    category_id: int

class SubThemeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    display_order: Optional[int] = Field(None, ge=0)

class SubThemeBase(BaseSchema):
    id: int
    name: str
    description: Optional[str]
    display_order: int
    category_id: int

class SubThemeResponse(SubThemeBase, TimestampSchema):
    pass

class SubThemeWithCategory(SubThemeResponse):
    category: CategoryBase

# This must be defined after SubThemeResponse
class CategoryWithSubThemes(CategoryResponse):
    sub_themes: List[SubThemeResponse] = []

# No need to rebuild as we define it after SubThemeResponse
