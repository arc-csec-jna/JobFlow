from app.database import Base
from sqlalchemy import JSON, Column, Integer, String,DateTime,Boolean
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from sqlalchemy.orm import relationship
import time

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

#executions = relationship("Execution", backref="job", cascade="all, delete-orphan")

    