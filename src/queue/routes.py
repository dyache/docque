import datetime
from typing import List, Annotated, Optional

from fastapi import APIRouter, HTTPException, Depends
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

from src.db import conn
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


class AssignedTicketResponse(BaseModel):
    queue_id: str
    position: int
    student_id: Optional[str]
    staff_id: str
    created_at: datetime.time
    status: str


@queue_router.post("/next", response_model=Optional[AssignedTicketResponse])
def assign_next_ticket(
        curr_user: Annotated[StaffSchema, Depends(auth_middleware)]):
    staff_id = str(curr_user.staff_id)
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Ensure staff exists
            cur.execute("SELECT staff_id FROM Staff WHERE staff_id = %s;", (staff_id,))
            staff = cur.fetchone()

            if not staff:
                raise HTTPException(status_code=404, detail="Staff member not found.")

            # Find the next available ticket (status = 'waiting') and lock it
            cur.execute("""
                    SELECT queue_id, position, student_id, created_at
                    FROM Queue
                    WHERE status = 'waiting'
                    ORDER BY position ASC
                    LIMIT 1
                    FOR UPDATE SKIP LOCKED;
                """)
            ticket = cur.fetchone()

            if not ticket:
                raise HTTPException(status_code=404, detail="No tickets available for assignment.")

            queue_id = ticket["queue_id"]
            position = ticket["position"]
            student_id = ticket["student_id"]
            created_at = ticket["created_at"]

            # Update the staff's current queue position
            cur.execute("""
                    UPDATE Staff
                    SET current_queue_number = %s
                    WHERE staff_id = %s;
                """, (position, staff_id))

            # Mark the ticket as 'in_progress'
            cur.execute("""
                    UPDATE Queue
                    SET status = 'in_progress'
                    WHERE queue_id = %s;
                """, (queue_id,))

            # Log the assignment in Queue_History
            cur.execute("""
                    INSERT INTO Queue_History (queue_id, position, student_id, created_at, status)
                    VALUES (%s, %s, %s, %s, 'in_progress');
                """, (queue_id, position, student_id, created_at))

            return {
                "queue_id": queue_id,
                "position": position,
                "student_id": student_id,
                "staff_id": staff_id,
                "created_at": created_at,
                "status": "in_progress"
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error assigning next ticket: {e}")
