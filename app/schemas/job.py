from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from app.enums.JobStatus import JobStatus

# this is the schema for the job model it defines what my APIP sends and receives

class JobCreate(BaseModel):
    title: str
    job_type: str
    payload: dict
    max_retries: int
    schedule_interval_seconds: int | None = None
    next_run_at: datetime | None = None
    enabled: bool = True
    priority: Literal["LOW","MEDIUM","HIGH"]
    status:Literal["PENDING","RUNNING","SUCCESS","FAILED"]
    user_id: int

class JobUpdate(BaseModel):
    title: str | None = None
    job_type: str | None = None
    payload: dict | None = None
    status: JobStatus | None = None


class JobResponse(BaseModel):
    id: int
    title: str
    job_type: str
    payload: dict
    status: str

    class ConfigDict:
        from_attributes = True