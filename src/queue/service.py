import datetime
import uuid
from typing import List

from src.queue.models import Queue
from src.queue.repository import QueueRepository
from src.queue.schema import QueueSchema
from src.queue_history.model import QueueHistory
from src.queue_history.repository import QueueHistoryRepository


class QueueService:
    def __init__(self, queue_repo: QueueRepository, queue_history: QueueHistoryRepository):
        self.queue_repo: QueueRepository = queue_repo
        self.queue_history_repo: QueueHistoryRepository = queue_history

    def create(self) -> uuid.UUID:
        queue_model = Queue(queue_id=uuid.uuid4(), created_at=datetime.datetime.now().timestamp(), status="on-wait")
        queue_to_insert = self.queue_repo.get_by_id(queue_model.queue_id)
        queue_history = QueueHistory(queue_id=queue_to_insert.queue_id, position=queue_to_insert.position,
                                     created_at=queue_to_insert.created_at, status=queue_to_insert.status)
        # TODO: make tx here
        self.queue_history_repo.create(queue_history)
        return self.queue_repo.create(queue_model)

    def get_all_sort_by_position(self) -> List[QueueSchema]:
        queue = self.queue_repo.get_all_sort_by_position()
        queue_schemas: List[QueueSchema] = []
        for q in queue:
            queue_schema = QueueSchema(status=q.status, position=q.position, queue_id=q.queue_id,
                                       created_at=q.created_at)
            queue_schemas.append(queue_schema)
        return queue_schemas
