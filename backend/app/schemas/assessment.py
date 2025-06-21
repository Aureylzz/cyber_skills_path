from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.schemas.base import BaseSchema
from app.models.enums import AssessmentStatus, QuestionType

class AssessmentStart(BaseModel):
    """Request to start a new assessment"""
    category_ids: Optional[List[int]] = None
    sub_theme_ids: Optional[List[int]] = None
    difficulty_levels: Optional[List[str]] = None

class AnswerSubmit(BaseModel):
    """Submit answer for a question"""
    question_id: int
    selected_option_ids: List[int] = Field(..., min_length=0)
    dont_know: bool = False
    time_spent_seconds: int = Field(..., ge=0)
    
    @field_validator('selected_option_ids')
    def validate_options(cls, v, info):
        if info.data.get('dont_know') and len(v) > 0:
            raise ValueError("Cannot select options when 'dont_know' is True")
        return v

class AssessmentSessionBase(BaseSchema):
    id: int
    user_id: int
    start_time: datetime
    end_time: Optional[datetime]
    status: AssessmentStatus
    total_score: float
    total_possible_score: float
    completion_percentage: float

class AssessmentSessionResponse(AssessmentSessionBase):
    duration_seconds: Optional[float]
    questions_answered: int
    questions_total: int

class QuestionInAssessment(BaseModel):
    """Question as presented during assessment"""
    id: int
    question_text: str
    question_type: QuestionType
    difficulty_level: str
    points: float
    options: List[Dict[str, Any]]  # id, text, display_order (no is_correct)
    category: str
    sub_theme: str

class AssessmentProgress(BaseModel):
    """Current progress in assessment"""
    session_id: int
    current_question: Optional[QuestionInAssessment]
    questions_answered: int
    questions_remaining: int
    score_earned: float
    time_elapsed_seconds: float

class AssessmentComplete(BaseModel):
    """Assessment completion summary"""
    session_id: int
    status: AssessmentStatus
    total_score: float
    total_possible_score: float
    percentage: float
    duration_seconds: float
    questions_answered: int
    questions_correct: int
    
class DifficultyProgress(BaseModel):
    """Progress for a difficulty level"""
    difficulty: str
    points: float
    questions_attempted: int
    questions_correct: int
    single_choice_correct: int
    multiple_choice_correct: int
    bonus_earned: bool
    score_earned: float

class CategoryProgress(BaseModel):
    """Progress for a category"""
    category_name: str
    questions_attempted: int
    questions_correct: int
    score_earned: float
    accuracy_percentage: float

class DetailedAssessmentReport(BaseModel):
    """Detailed assessment report"""
    session: AssessmentSessionResponse
    difficulty_breakdown: List[DifficultyProgress]
    category_breakdown: List[CategoryProgress]
    sub_theme_breakdown: List[Dict[str, Any]]
    question_details: List[Dict[str, Any]]
