from sqlalchemy import Column, String, Text, Table, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import IdMixin, TimestampMixin

# Association table for many-to-many relationship
question_tag_mapping = Table(
    'question_tag_mapping',
    Base.metadata,
    Column('question_id', Integer, ForeignKey('questions.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('question_tags.id'), primary_key=True)
)

class QuestionTag(Base, IdMixin, TimestampMixin):
    __tablename__ = "question_tags"
    
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    
    # Relationships
    questions = relationship(
        "Question",
        secondary=question_tag_mapping,
        back_populates="tags"
    )
