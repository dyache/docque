from fastapi import FastAPI

from src.queue.routes import queue_router
from src.queue_history.routes import queue_history_router
from src.staff.routes import staff_router
from src.student.routes import student_router

# TODO: protect all other routes with auth

app = FastAPI(root_path="/api/v1", title="docque API", description="This is qocque queue API", version="1.0.0")
app.include_router(prefix="/queue", router=queue_router)
app.include_router(prefix="/staff", router=staff_router)
app.include_router(prefix="/history", router=queue_history_router)
app.include_router(prefix="/student", router=student_router)
