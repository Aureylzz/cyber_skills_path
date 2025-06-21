from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import IdMixin, TimestampMixin

class SubTheme(Base, IdMixin, TimestampMixin):
    __tablename__ = "sub_themes"
    
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    display_order = Column(Integer, nullable=False)
    
    # Relationships
    category = relationship("Category", back_populates="sub_themes")
    questions = relationship(
        "Question", 
        back_populates="sub_theme",
        cascade="all, delete-orphan"
    )
