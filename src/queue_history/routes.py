from typing import List
from fastapi import APIRouter, HTTPException, status

from src.queue_history.schema import QueueHistorySchema
from src.queue_history.service import QueueHistoryService

queue_history_router = APIRouter()

class QueueHistoryRoutes:
    def __init__(self, queue_history_serv: QueueHistoryService):
        self.queue_history_serv = queue_history_serv

    @queue_history_router.get("/history/")
    def get_all(self) -> List[QueueHistorySchema]:
        try:
            return self.queue_history_serv.get_all_sort_by_created_at()
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            ) from exc
