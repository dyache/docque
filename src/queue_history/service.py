from typing import Annotated
from typing import List, Optional

from fastapi import Depends

from src.custom_exception import DataException
from src.db import cur, conn
from src.queue_history.repository import QueueHistoryRepository
from src.queue_history.schema import QueueHistorySchema


class QueueHistoryService:
    def __init__(self, queue_repo: QueueHistoryRepository):
        self.queue_repo = queue_repo

    def get_all_sort_by_created_at(self) -> Optional[List[QueueHistorySchema]]:
        try:
            queue_history = self.queue_repo.get_all_sort_by_created_at()
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
            print(str(e))
            raise DataException("error getting all tickets")


def get_queue_history_service() -> QueueHistoryService:
    return QueueHistoryService(QueueHistoryRepository(conn, cur))


QueueHistoryServiceDep = Annotated[QueueHistoryService, Depends(get_queue_history_service)]
