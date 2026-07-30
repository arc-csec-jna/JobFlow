from app.core.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String,DateTime
from sqlalchemy.orm import relationship

class Execution(Base):
    __tablename__ = "executions"

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    attempt_number = Column(Integer, default=1)
    status = Column(String, default="PENDING")
    started_at = Column(DateTime)
    finished_at = Column(DateTime)
    error_message = Column(String)
    job = relationship("Job", back_populates="executions")
    logs = relationship("Log", back_populates="executions")