from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from .database import Base

class WorkItem(Base):
    __tablename__ = "work_items"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    employee_id = Column(Integer, nullable=False, index=True)
    status = Column(String(20), nullable=False, default="TODO")
    priority = Column(String(20), nullable=False, default="MEDIUM")
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)