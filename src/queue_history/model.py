import datetime
import uuid


class QueueHistory:
    def __init__(self, queue_id: uuid.UUID, position: int, created_at: datetime.time, status: str):
        self.queue_id: uuid.UUID = queue_id
        self.position: int = position
        self.status: str = status
        self.created_at: datetime.time = created_at
