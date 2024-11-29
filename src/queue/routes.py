from typing import List

from fastapi import APIRouter

from src.queue.schema import QueueSchema
from src.queue.service import QueueService

queue_router = APIRouter()


class QueueRoutes:
    def __init__(self, queue_serv: QueueService):
        self.queue_serv: QueueService = queue_serv

    @queue_router.post("/queue/")
    def create(self):
        return self.queue_serv.create()

    @queue_router.get("/queue/")
    def get_all(self) -> List[QueueSchema]:
        return self.queue_serv.get_all_sort_by_position()
