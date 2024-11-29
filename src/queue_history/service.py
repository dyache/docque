from typing import List

from src.queue.repository import QueueRepository
from src.queue_history.schema import QueueHistorySchema


class QueueHistoryService:
    def __init__(self, queue_repo: QueueRepository):
        self.queue_repo = queue_repo

    def get_all_sort_by_created_at(self) -> List[QueueHistorySchema]:
        queue_history = self.queue_repo.get_all_sort_by_position()
        queue_history_schemas: List[QueueHistorySchema] = []
        for q in queue_history:
            queue_history_schema = QueueHistorySchema(created_at=q.created_at, queue_id=q.queue_id, position=q.position,
                                                      status=q.status)
            queue_history_schemas.append(queue_history_schema)
        return queue_history_schemas
