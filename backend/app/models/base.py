from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declared_attr

class TimestampMixin:
    """Mixin that adds created_at and updated_at timestamps to models"""
    
    @declared_attr
    def created_at(cls):
        return Column(DateTime, server_default=func.now(), nullable=False)
    
    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime, 
            server_default=func.now(), 
            onupdate=func.now(), 
            nullable=False
        )

class IdMixin:
    """Mixin that adds an auto-incrementing id primary key"""
    
    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True, index=True)
