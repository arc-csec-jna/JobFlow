from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.enums import Priority


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    job_type = Column(String, nullable=False)
    payload = Column(JSONB, nullable=False) 
    status = Column(String, default="ACTIVE")
    max_retries = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.now)
    executions = relationship("Execution", back_populates="job")
    schedule_interval_seconds = Column(Integer,nullable=True)
    next_run_at = Column(DateTime, nullable=True)
    enabled = Column(Boolean,default=True)
    priority = Column(Integer,default=Priority.MEDIUM.value)
    retry_count = Column(Integer, default=0, nullable=False)

#executions = relationship("Execution", backref="job", cascade="all, delete-orphan")

    