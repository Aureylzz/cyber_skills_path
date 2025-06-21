from sqlalchemy import Column, Integer, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import IdMixin

class CategoryProgress(Base, IdMixin):
    __tablename__ = "category_progress"
    
    session_id = Column(Integer, ForeignKey("assessment_sessions.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    questions_attempted = Column(Integer, default=0, nullable=False)
    questions_correct = Column(Integer, default=0, nullable=False)
    score_earned = Column(Numeric(10, 2), default=0, nullable=False)
    
    # Relationships
    session = relationship("AssessmentSession", back_populates="category_progress")
    category = relationship("Category")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint(
            "session_id", 
            "category_id", 
            name="unique_session_category"
        ),
    )
    
    @property
    def accuracy_percentage(self):
        if self.questions_attempted == 0:
            return 0
        return (self.questions_correct / self.questions_attempted) * 100
