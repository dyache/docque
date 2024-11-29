from fastapi import FastAPI

from src.queue.routes import queue_router
from src.queue_history.routes import queue_history_router
from src.staff.routes import staff_router

app = FastAPI(root_path="/api/v1", title="docque API", description="This is qocque queue API", version="1.0.0")
app.include_router(queue_router)
app.include_router(staff_router)
app.include_router(queue_history_router)
