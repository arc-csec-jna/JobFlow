from datetime import datetime
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    role: str | None = None
    is_active: bool | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    role: str

    model_config = {"from_attributes": True}
