from pydantic import BaseModel

class ExecutionResult(BaseModel):
    status: str
    message: str
