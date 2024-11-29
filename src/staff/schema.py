import uuid

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