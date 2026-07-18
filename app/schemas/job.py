from pydantic import BaseModel
from datetime import datetime
# this is the schema for the job model it defines what my APIP sends and receives

class JobCreate(BaseModel):
    title: str
    job_type: str
    payload: dict
    max_retries: int

    schedule_interval_seconds: int | None = None
    next_run_at: datetime | None = None
    enabled: bool = True

class JobUpdate(BaseModel):
    title: str | None = None
    job_type: str | None = None
    payload: dict | None = None
    status: str | None = None


class JobResponse(BaseModel):
    id: int
    title: str
    job_type: str
    payload: dict
    status: str

    class Config:
        from_attributes = True