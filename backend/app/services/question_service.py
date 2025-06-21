from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from app.models import Question, AnswerOption, SubTheme, QuestionTag, question_tag_mapping
from app.schemas import QuestionCreate, QuestionUpdate, AnswerOptionCreate
from app.models.enums import QuestionType

class QuestionService:
    @staticmethod
    async def create_question(
        db: AsyncSession,
        question_data: QuestionCreate,
        created_by_id: int
    ) -> Question:
        """Create a new question with answer options"""
        # Verify sub-theme exists
        sub_theme_result = await db.execute(
            select(SubTheme).where(SubTheme.id == question_data.sub_theme_id)
        )
        if not sub_theme_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sub-theme not found"
            )
        
        # Create question
        question_dict = question_data.model_dump(exclude={"answer_options"})
        question_dict["created_by"] = created_by_id
        question_dict["updated_by"] = created_by_id
        
        question = Question(**question_dict)
        db.add(question)
        await db.flush()  # Get the question ID
        
        # Create answer options
        for idx, option_data in enumerate(question_data.answer_options):
            option = AnswerOption(
                question_id=question.id,
                option_text=option_data.option_text,
                is_correct=option_data.is_correct,
                display_order=option_data.display_order
            )
            db.add(option)
        
        await db.commit()
        await db.refresh(question)
        
        # Load answer options
        await db.execute(
            select(Question)
            .where(Question.id == question.id)
            .options(selectinload(Question.answer_options))
        )
        
        return question
    
    @staticmethod
    async def get_questions(
        db: AsyncSession,
        sub_theme_id: Optional[int] = None,
        difficulty_level: Optional[str] = None,
        question_type: Optional[str] = None,
        is_active: Optional[bool] = True,
        skip: int = 0,
        limit: int = 100
    ) -> List[Question]:
        """Get questions with filters"""
        query = select(Question).options(
            selectinload(Question.answer_options),
            selectinload(Question.sub_theme)
        )
        
        # Apply filters
        if sub_theme_id:
            query = query.where(Question.sub_theme_id == sub_theme_id)
        if difficulty_level:
            query = query.where(Question.difficulty_level == difficulty_level)
        if question_type:
            query = query.where(Question.question_type == question_type)
        if is_active is not None:
            query = query.where(Question.is_active == is_active)
        
        query = query.offset(skip).limit(limit).order_by(Question.id)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_question(
        db: AsyncSession,
        question_id: int,
        include_details: bool = False
    ) -> Optional[Question]:
        """Get a single question by ID"""
        query = select(Question).where(Question.id == question_id)
        
        # Always include answer options
        query = query.options(selectinload(Question.answer_options))
        
        if include_details:
            query = query.options(
                selectinload(Question.sub_theme).selectinload(SubTheme.category),
                selectinload(Question.tags)
            )
        
        result = await db.execute(query)
        question = result.scalar_one_or_none()
        
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )
        
        return question
    
    @staticmethod
    async def update_question(
        db: AsyncSession,
        question_id: int,
        question_data: QuestionUpdate,
        updated_by_id: int
    ) -> Question:
        """Update a question (not answer options)"""
        question = await QuestionService.get_question(db, question_id)
        
        # Update only provided fields
        update_data = question_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(question, field, value)
        
        question.updated_by = updated_by_id
        
        await db.commit()
        await db.refresh(question)
        return question
    
    @staticmethod
    async def delete_question(
        db: AsyncSession,
        question_id: int
    ) -> dict:
        """Delete a question (cascades to answer options)"""
        question = await QuestionService.get_question(db, question_id)
        
        await db.delete(question)
        await db.commit()
        
        return {"message": f"Question {question_id} deleted successfully"}
    
    @staticmethod
    async def toggle_question_active(
        db: AsyncSession,
        question_id: int,
        updated_by_id: int
    ) -> Question:
        """Toggle question active status"""
        question = await QuestionService.get_question(db, question_id)
        
        question.is_active = not question.is_active
        question.updated_by = updated_by_id
        
        await db.commit()
        await db.refresh(question)
        return question
    
    @staticmethod
    async def get_questions_by_category(
        db: AsyncSession,
        category_id: int,
        difficulty_level: Optional[str] = None,
        is_active: bool = True
    ) -> List[Question]:
        """Get all questions in a category"""
        query = select(Question).join(SubTheme).where(
            and_(
                SubTheme.category_id == category_id,
                Question.is_active == is_active
            )
        ).options(
            selectinload(Question.answer_options),
            selectinload(Question.sub_theme)
        )
        
        if difficulty_level:
            query = query.where(Question.difficulty_level == difficulty_level)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def validate_question_answers(question: Question) -> bool:
        """Validate question has correct number of correct answers"""
        correct_count = sum(1 for opt in question.answer_options if opt.is_correct)
        
        if question.question_type == QuestionType.SINGLE_CHOICE:
            return correct_count == 1
        elif question.question_type == QuestionType.MULTIPLE_CHOICE:
            return 1 <= correct_count <= 4
        
        return False