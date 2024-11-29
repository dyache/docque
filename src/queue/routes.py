from typing import List
from fastapi import APIRouter, HTTPException
from src.queue.schema import QueueSchema
from src.queue.service import QueueService

queue_router = APIRouter()

class QueueRoutes:
    def __init__(self, queue_serv: QueueService):
        self.queue_serv: QueueService = queue_serv

    @queue_router.post("/queue/")
    def create(self):
        try:
            return self.queue_serv.create()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while creating the queue: {e}")

    @queue_router.get("/queue/")
    def get_all(self) -> List[QueueSchema]:
        try:
            return self.queue_serv.get_all_sort_by_position()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the queue: {e}")
