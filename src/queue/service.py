import datetime
import uuid
from typing import List, Optional, Annotated

from fastapi import Depends

from src.db import cur, conn
from src.queue.models import Queue
from src.queue.repository import QueueRepository
from src.queue.schema import QueueSchema
from src.queue_history.model import QueueHistory
from src.queue_history.repository import QueueHistoryRepository


class QueueService:
    def __init__(self, queue_repo: QueueRepository, queue_history_repo: QueueHistoryRepository):
        self.queue_repo: QueueRepository = queue_repo
        self.queue_history_repo: QueueHistoryRepository = queue_history_repo

    def create(self, student_id: str) -> Optional[uuid.UUID]:
        try:
            queue_model = Queue(queue_id=uuid.uuid4(), created_at=datetime.datetime.now(),
                                status="on-wait",
                                position=0, student_id=student_id)

            # TODO: make tx here
            self.queue_repo.create(queue_model)
            queue_history = QueueHistory(queue_id=queue_model.queue_id, position=queue_model.position,
                                         created_at=queue_model.created_at, status=queue_model.status)
            return self.queue_history_repo.create(queue_history)


        except Exception as e:
            print(f"An error occurred while creating the queue: {e}")
            return None

    def get_all_sort_by_position(self) -> Optional[List[QueueSchema]]:
        try:
            queue = self.queue_repo.get_all_sort_by_position()
            queue_schemas: List[QueueSchema] = []
            for q in queue:
                queue_schema = QueueSchema(status=q.status, position=q.position, queue_id=q.queue_id,
                                           created_at=q.created_at)
                queue_schemas.append(queue_schema)
            return queue_schemas
        except Exception as e:
            print(f"An error occurred while retrieving the queue: {e}")
            return None


def get_queue_service() -> QueueService:
    return QueueService(QueueRepository(conn, cur), QueueHistoryRepository(conn, cur))


QueueServiceDep = Annotated[QueueService, Depends(get_queue_service)]
