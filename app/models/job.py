from app.database import Base
from sqlalchemy import JSON, Column, Integer, String,DateTime
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from sqlalchemy.orm import relationship

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

#executions = relationship("Execution", backref="job", cascade="all, delete-orphan")

    