import uuid
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    staff_id: uuid.UUID | None = None


class StaffSchema(BaseModel):
    staff_id: uuid.UUID
    name: str

class StaffCreateSchema(BaseModel):
    name: str
    password: str
    
class StaffUpdateSchema(BaseModel):
    staff_id: uuid.UUID
    name: Optional[str] = None
    password: Optional[str] = None
    current_queue_number: Optional[int] = None
