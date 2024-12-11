import datetime
import uuid

from pydantic import BaseModel


class QueueSchema(BaseModel):
    queue_id: uuid.UUID
    position: int
    status: str
    created_at: datetime.datetime


class QueueCreateSchema(BaseModel):
    student_id: str
