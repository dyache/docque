from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Depends

from src.queue.schema import QueueSchema, QueueCreateSchema
from src.queue.service import QueueServiceDep
from src.staff.middleware import auth_middleware
from src.staff.schema import StaffSchema

queue_router = APIRouter()


@queue_router.post("/")
def create(queue_serv: QueueServiceDep,
           queue: QueueCreateSchema,
           curr_user: Annotated[StaffSchema, Depends(auth_middleware)]
           ):
    try:
        return queue_serv.create(queue.student_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the queue: {e}")


@queue_router.get("/")
def get_all(queue_serv: QueueServiceDep,
            curr_user: Annotated[StaffSchema, Depends(auth_middleware)]
            ) -> List[QueueSchema]:
    try:
        return queue_serv.get_all_sort_by_position()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the queue: {e}")
