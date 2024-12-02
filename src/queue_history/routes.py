from typing import List
from fastapi import APIRouter, HTTPException, status

from src.queue_history.schema import QueueHistorySchema
from src.queue_history.service import QueueHistoryServiceDep

queue_history_router = APIRouter()

@queue_history_router.get("/history/")
def get_all(queue_history_serv: QueueHistoryServiceDep) -> List[QueueHistorySchema]:
    try:
        return queue_history_serv.get_all_sort_by_created_at()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from exc
