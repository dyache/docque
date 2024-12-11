import datetime
import uuid


class Queue:
    def __init__(self, queue_id: uuid.UUID, position: int, student_id: str, created_at: datetime.time, status: str):
        self.queue_id: uuid.UUID = queue_id
        self.position: int = position
        self.student_id: str = student_id
        self.status: str = status
        self.created_at: datetime.time = created_at
