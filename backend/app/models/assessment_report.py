from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Enum, func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import IdMixin
from app.models.enums import ReportType

class AssessmentReport(Base, IdMixin):
    __tablename__ = "assessment_reports"
    
    session_id = Column(Integer, ForeignKey("assessment_sessions.id"), nullable=False)
    report_type = Column(Enum(ReportType), nullable=False)
    generated_at = Column(DateTime, server_default=func.now(), nullable=False)
    report_data = Column(JSON)  # Stores structured report data
    pdf_path = Column(String(500))  # Path to generated PDF if applicable
    
    # Relationships
    session = relationship("AssessmentSession", back_populates="reports")
