from pydantic import BaseModel


class ExecutionCreate(BaseModel):
    job_id: int
    status: str
    result: str = None

class ExecutionUpdate(BaseModel):
    result: str = None

class Execution(ExecutionCreate):
    id: int

    class Config:
        from_attributes = True