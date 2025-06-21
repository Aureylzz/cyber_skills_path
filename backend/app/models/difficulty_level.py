from sqlalchemy import Column, Integer, String, Numeric, Text
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import IdMixin

class DifficultyLevel(Base, IdMixin):
    __tablename__ = "difficulty_levels"
    
    name = Column(String(50), unique=True, nullable=False)
    points = Column(Numeric(3, 1), nullable=False)
    level_order = Column(Integer, nullable=False, index=True)
    description = Column(Text)
    
    # Relationships
    progress_records = relationship(
        "DifficultyLevelProgress", 
        back_populates="difficulty_level"
    )
