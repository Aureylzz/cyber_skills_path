from sqlalchemy import Column, Integer, Boolean, DateTime, Numeric, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import IdMixin

class UserResponse(Base, IdMixin):
    __tablename__ = "user_responses"
    
    session_id = Column(Integer, ForeignKey("assessment_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    response_time = Column(DateTime, server_default=func.now(), nullable=False)
    time_spent_seconds = Column(Integer, default=0, nullable=False)
    dont_know = Column(Boolean, default=False, nullable=False)
    score_earned = Column(Numeric(10, 2), default=0, nullable=False)
    
    # Relationships
    session = relationship("AssessmentSession", back_populates="user_responses")
    question = relationship("Question", back_populates="user_responses")
    response_answers = relationship(
        "ResponseAnswer", 
        back_populates="user_response",
        cascade="all, delete-orphan"
    )
    
    # Constraints
    __table_args__ = (
        UniqueConstraint("session_id", "question_id", name="unique_session_question"),
    )
