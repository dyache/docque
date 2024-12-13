from typing import List, Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from src.custom_exception import DataException
from src.queue_history.schema import QueueHistorySchema
from src.queue_history.service import QueueHistoryServiceDep
from src.staff.middleware import auth_middleware
from src.staff.schema import StaffSchema

queue_history_router = APIRouter()


@queue_history_router.get("/")
def get_all(queue_history_serv: QueueHistoryServiceDep,
            curr_user: Annotated[StaffSchema, Depends(auth_middleware)]) -> List[QueueHistorySchema]:
    try:
        return queue_history_serv.get_all_sort_by_created_at()
    except DataException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from exc
