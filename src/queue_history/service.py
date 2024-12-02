from typing import List, Optional
from src.queue.repository import QueueRepository
from src.queue_history.schema import QueueHistorySchema
from src.db import cur, conn
from fastapi import Depends
from typing import Annotated
from src.queue_history.repository import QueueHistoryRepository

class QueueHistoryService:
    def __init__(self, queue_repo: QueueRepository):
        self.queue_repo = queue_repo

    def get_all_sort_by_created_at(self) -> Optional[List[QueueHistorySchema]]:
        try:
            queue_history = self.queue_repo.get_all_sort_by_position()
            queue_history_schemas: List[QueueHistorySchema] = []
            for q in queue_history:
                queue_history_schema = QueueHistorySchema(
                    created_at=q.created_at, 
                    queue_id=q.queue_id, 
                    position=q.position,
                    status=q.status
                )
                queue_history_schemas.append(queue_history_schema)
            return queue_history_schemas
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

def get_queue_history_service() -> QueueHistoryService:
    return QueueHistoryService(QueueHistoryRepository(conn,cur), QueueRepository(conn, cur))
QueueHistoryServiceDep = Annotated[QueueHistoryService, Depends(get_queue_history_service)]
