from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime,Text
from datetime import datetime
from sqlalchemy.orm import relationship

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

    execution = relationship("Execution", back_populates="logs")