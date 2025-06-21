from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import IdMixin

class ResponseAnswer(Base, IdMixin):
    __tablename__ = "response_answers"
    
    user_response_id = Column(Integer, ForeignKey("user_responses.id"), nullable=False)
    answer_option_id = Column(Integer, ForeignKey("answer_options.id"), nullable=False)
    
    # Relationships
    user_response = relationship("UserResponse", back_populates="response_answers")
    answer_option = relationship("AnswerOption", back_populates="response_answers")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint(
            "user_response_id", 
            "answer_option_id", 
            name="unique_response_answer"
        ),
    )
