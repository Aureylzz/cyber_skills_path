from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import IdMixin, TimestampMixin
from app.models.enums import QuestionType, DifficultyLevel

class Question(Base, IdMixin, TimestampMixin):
    __tablename__ = "questions"
    
    sub_theme_id = Column(Integer, ForeignKey("sub_themes.id"), nullable=False)
    difficulty_level = Column(Enum(DifficultyLevel), nullable=False)
    question_type = Column(Enum(QuestionType), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    rationale = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    sub_theme = relationship("SubTheme", back_populates="questions")
    answer_options = relationship(
        "AnswerOption", 
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="AnswerOption.display_order"
    )
    user_responses = relationship(
        "UserResponse", 
        back_populates="question"
    )
    tags = relationship(
        "QuestionTag",
        secondary="question_tag_mapping",
        back_populates="questions"
    )
    
    @property
    def points(self):
        return self.difficulty_level.points
    
    @property
    def correct_answers(self):
        return [opt for opt in self.answer_options if opt.is_correct]
