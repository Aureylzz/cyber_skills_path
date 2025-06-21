from sqlalchemy import Column, Integer, String, DateTime, Enum, Numeric, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import IdMixin
from app.models.enums import AssessmentStatus

class AssessmentSession(Base, IdMixin):
    __tablename__ = "assessment_sessions"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime, server_default=func.now(), nullable=False)
    end_time = Column(DateTime, nullable=True)
    status = Column(
        Enum(AssessmentStatus), 
        default=AssessmentStatus.IN_PROGRESS, 
        nullable=False,
        index=True
    )
    total_score = Column(Numeric(10, 2), default=0, nullable=False)
    total_possible_score = Column(Numeric(10, 2), default=0, nullable=False)
    completion_percentage = Column(Numeric(5, 2), default=0, nullable=False)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="assessment_sessions")
    user_responses = relationship(
        "UserResponse", 
        back_populates="session",
        cascade="all, delete-orphan"
    )
    difficulty_progress = relationship(
        "DifficultyLevelProgress", 
        back_populates="session",
        cascade="all, delete-orphan"
    )
    category_progress = relationship(
        "CategoryProgress", 
        back_populates="session",
        cascade="all, delete-orphan"
    )
    sub_theme_progress = relationship(
        "SubThemeProgress", 
        back_populates="session",
        cascade="all, delete-orphan"
    )
    reports = relationship(
        "AssessmentReport", 
        back_populates="session",
        cascade="all, delete-orphan"
    )
    
    @property
    def duration_seconds(self):
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
