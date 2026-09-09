from pydantic import BaseModel


class LogCreate(BaseModel):
    execution_id: int
    level: str
    message: str


class LogResponse(BaseModel):
    id: int
    execution_id: int
    level: str
    message: str

    class Config:
        from_attributes = True