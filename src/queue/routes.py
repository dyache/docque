from typing import List

from fastapi import APIRouter, HTTPException

from src.queue.schema import QueueSchema
from src.queue.service import QueueServiceDep

queue_router = APIRouter()


@queue_router.post("/")
def create(queue_serv: QueueServiceDep):
    try:
        return queue_serv.create()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the queue: {e}")


@queue_router.get("/")
def get_all(queue_serv: QueueServiceDep) -> List[QueueSchema]:
    try:
        return queue_serv.get_all_sort_by_position()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the queue: {e}")
