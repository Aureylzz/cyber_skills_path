from typing import List, Annotated, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import (
    QuestionCreate, QuestionUpdate, QuestionResponse, 
    QuestionWithDetails, PaginationParams
)
from app.services.question_service import QuestionService
from app.core.dependencies import get_current_user_optional, get_instructor_user, get_admin_user
from app.models import User

router = APIRouter()

@router.post("/", response_model=QuestionResponse)
async def create_question(
    question_data: QuestionCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    instructor: Annotated[User, Depends(get_instructor_user)]
):
    """Create a new question (Instructor/Admin only)"""
    return await QuestionService.create_question(
        db, question_data, instructor.id
    )

@router.get("/", response_model=List[QuestionResponse])
async def get_questions(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[Optional[User], Depends(get_current_user_optional)],
    sub_theme_id: Optional[int] = Query(None),
    difficulty_level: Optional[str] = Query(None),
    question_type: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get questions with filters (Public, but only active questions for non-authenticated users)"""
    # Non-authenticated users only see active questions
    if not current_user and is_active is None:
        is_active = True
    elif is_active is None:
        is_active = None  # Authenticated users see all by default
    
    return await QuestionService.get_questions(
        db, sub_theme_id, difficulty_level, 
        question_type, is_active, skip, limit
    )

@router.get("/{question_id}", response_model=QuestionWithDetails)
async def get_question(
    question_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[Optional[User], Depends(get_current_user_optional)]
):
    """Get a single question with details (Public)"""
    question = await QuestionService.get_question(
        db, question_id, include_details=True
    )
    
    # Check if user can see inactive questions
    if not question.is_active and (not current_user or current_user.role.value == "student"):
        raise HTTPException(
            status_code=403,
            detail="This question is not available"
        )
    
    return question

@router.put("/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: int,
    question_data: QuestionUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    instructor: Annotated[User, Depends(get_instructor_user)]
):
    """Update a question (Instructor/Admin only)"""
    return await QuestionService.update_question(
        db, question_id, question_data, instructor.id
    )

@router.post("/{question_id}/toggle-active", response_model=QuestionResponse)
async def toggle_question_active(
    question_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    instructor: Annotated[User, Depends(get_instructor_user)]
):
    """Toggle question active status (Instructor/Admin only)"""
    return await QuestionService.toggle_question_active(
        db, question_id, instructor.id
    )

@router.delete("/{question_id}")
async def delete_question(
    question_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(get_admin_user)]
):
    """Delete a question (Admin only)"""
    return await QuestionService.delete_question(db, question_id)

@router.get("/by-category/{category_id}", response_model=List[QuestionResponse])
async def get_questions_by_category(
    category_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[Optional[User], Depends(get_current_user_optional)],
    difficulty_level: Optional[str] = Query(None)
):
    """Get all questions in a category (Public)"""
    # Non-authenticated users only see active questions
    is_active = True if not current_user else None
    
    return await QuestionService.get_questions_by_category(
        db, category_id, difficulty_level, is_active
    )
