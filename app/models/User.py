from app.core.database import Base

from  sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")  # e.g., 'user', 'admin'
    is_active = Column(Boolean,default=True,nullable=False)
    created_at = Column(DateTime, default=datetime.now(tz=timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(tz=timezone.utc), onupdate=datetime.now(tz=timezone.utc))

    jobs = relationship("Job", back_populates="user")  # Assuming a user can have multiple jobs