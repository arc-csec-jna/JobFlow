from datetime import datetime

from pydantic import BaseModel


class ExecutionCreate(BaseModel):
    status: str

class ExecutionUpdate(BaseModel):
    status: str = None

class ExecutionResponse(BaseModel):
    id: int
    job_id: int
    status: str
    attempt_number: int
    started_at: datetime | None
    finished_at: datetime | None
    error_message: str | None
    
    class Config:
        from_attributes = True

