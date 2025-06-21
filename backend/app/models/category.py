from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import IdMixin, TimestampMixin

class Category(Base, IdMixin, TimestampMixin):
    __tablename__ = "categories"
    
    name = Column(String(100), nullable=False)
    display_order = Column(Integer, nullable=False, index=True)
    
    # Relationships
    sub_themes = relationship(
        "SubTheme", 
        back_populates="category",
        cascade="all, delete-orphan",
        order_by="SubTheme.display_order"
    )
