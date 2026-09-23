from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)

    execution_id = Column(
        Integer,
        ForeignKey("executions.id")
    )

    level = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime,default=datetime.now)

    executions = relationship("Execution", back_populates="logs")