from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import IdMixin, TimestampMixin

class AnswerOption(Base, IdMixin, TimestampMixin):
    __tablename__ = "answer_options"
    
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    option_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False, nullable=False)
    display_order = Column(Integer, nullable=False)
    
    # Relationships
    question = relationship("Question", back_populates="answer_options")
    response_answers = relationship(
        "ResponseAnswer", 
        back_populates="answer_option"
    )
