from sqlalchemy import Column, Integer, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import IdMixin

class SubThemeProgress(Base, IdMixin):
    __tablename__ = "sub_theme_progress"
    
    session_id = Column(Integer, ForeignKey("assessment_sessions.id"), nullable=False)
    sub_theme_id = Column(Integer, ForeignKey("sub_themes.id"), nullable=False)
    questions_attempted = Column(Integer, default=0, nullable=False)
    questions_correct = Column(Integer, default=0, nullable=False)
    score_earned = Column(Numeric(10, 2), default=0, nullable=False)
    
    # Relationships
    session = relationship("AssessmentSession", back_populates="sub_theme_progress")
    sub_theme = relationship("SubTheme")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint(
            "session_id", 
            "sub_theme_id", 
            name="unique_session_subtheme"
        ),
    )
