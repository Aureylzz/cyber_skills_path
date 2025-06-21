from sqlalchemy import Column, Integer, Boolean, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import IdMixin

class DifficultyLevelProgress(Base, IdMixin):
    __tablename__ = "difficulty_level_progress"
    
    session_id = Column(Integer, ForeignKey("assessment_sessions.id"), nullable=False)
    difficulty_level_id = Column(Integer, ForeignKey("difficulty_levels.id"), nullable=False)
    questions_attempted = Column(Integer, default=0, nullable=False)
    questions_correct = Column(Integer, default=0, nullable=False)
    single_choice_correct = Column(Integer, default=0, nullable=False)
    multiple_choice_correct = Column(Integer, default=0, nullable=False)
    bonus_earned = Column(Boolean, default=False, nullable=False)
    score_earned = Column(Numeric(10, 2), default=0, nullable=False)
    
    # Relationships
    session = relationship("AssessmentSession", back_populates="difficulty_progress")
    difficulty_level = relationship("DifficultyLevel", back_populates="progress_records")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint(
            "session_id", 
            "difficulty_level_id", 
            name="unique_session_difficulty"
        ),
    )
    
    @property
    def is_bonus_eligible(self):
        """Check if all 4 questions (2 single, 2 multiple) are correct"""
        return (self.single_choice_correct == 2 and 
                self.multiple_choice_correct == 2 and
                self.questions_correct == 4)
