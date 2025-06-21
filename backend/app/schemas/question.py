from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from app.schemas.base import BaseSchema, TimestampSchema
from app.models.enums import QuestionType, DifficultyLevel

class AnswerOptionCreate(BaseModel):
    option_text: str = Field(..., min_length=1)
    is_correct: bool = False
    display_order: int = Field(..., ge=0)

class AnswerOptionUpdate(BaseModel):
    option_text: Optional[str] = Field(None, min_length=1)
    is_correct: Optional[bool] = None
    display_order: Optional[int] = Field(None, ge=0)

class AnswerOptionResponse(BaseSchema):
    id: int
    option_text: str
    is_correct: bool
    display_order: int

class QuestionCreate(BaseModel):
    sub_theme_id: int
    difficulty_level: DifficultyLevel
    question_type: QuestionType
    question_text: str = Field(..., min_length=10)
    rationale: str = Field(..., min_length=10)
    answer_options: List[AnswerOptionCreate] = Field(..., min_length=4, max_length=4)
    
    @field_validator('answer_options')
    def validate_answer_options(cls, v, info):
        question_type = info.data.get('question_type')
        correct_count = sum(1 for opt in v if opt.is_correct)
        
        if question_type == QuestionType.SINGLE_CHOICE:
            if correct_count != 1:
                raise ValueError("Single choice questions must have exactly 1 correct answer")
        elif question_type == QuestionType.MULTIPLE_CHOICE:
            if correct_count < 1 or correct_count > 4:
                raise ValueError("Multiple choice questions must have 1-4 correct answers")
        
        return v

class QuestionUpdate(BaseModel):
    question_text: Optional[str] = Field(None, min_length=10)
    rationale: Optional[str] = Field(None, min_length=10)
    is_active: Optional[bool] = None

class QuestionBase(BaseSchema):
    id: int
    sub_theme_id: int
    difficulty_level: DifficultyLevel
    question_type: QuestionType
    question_text: str
    rationale: str
    is_active: bool
    points: float

class QuestionResponse(QuestionBase, TimestampSchema):
    answer_options: List[AnswerOptionResponse] = []

class QuestionWithDetails(QuestionResponse):
    sub_theme: "SubThemeBase"
    tags: List["QuestionTagBase"] = []

# Question tag schemas
class QuestionTagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None

class QuestionTagBase(BaseSchema):
    id: int
    name: str
    description: Optional[str]

class QuestionTagResponse(QuestionTagBase, TimestampSchema):
    pass

# Import at the end to avoid circular imports
from app.schemas.category import SubThemeBase
QuestionWithDetails.model_rebuild()