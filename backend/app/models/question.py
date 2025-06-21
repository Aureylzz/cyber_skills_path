from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import TimestampMixin
import enum

class QuestionType(str, enum.Enum):
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"

class DifficultyLevel(str, enum.Enum):
    NOVICE = "novice"
    AMATEUR = "amateur"
    INITIATE = "initiate"
    PROFESSIONAL = "professional"
    EXPERT = "expert"

class Question(Base, TimestampMixin):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True)
    sub_theme_id = Column(Integer, ForeignKey("sub_themes.id"), nullable=False)
    difficulty_level = Column(Enum(DifficultyLevel), nullable=False)
    question_type = Column(Enum(QuestionType), nullable=False)
    question_text = Column(Text, nullable=False)
    rationale = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    sub_theme = relationship("SubTheme", back_populates="questions")
    answer_options = relationship("AnswerOption", back_populates="question", cascade="all, delete-orphan")
    
    @property
    def points(self):
        points_map = {
            DifficultyLevel.NOVICE: 0.5,
            DifficultyLevel.AMATEUR: 1.0,
            DifficultyLevel.INITIATE: 2.0,
            DifficultyLevel.PROFESSIONAL: 3.5,
            DifficultyLevel.EXPERT: 5.5
        }
        return points_map[self.difficulty_level]