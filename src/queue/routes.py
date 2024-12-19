import datetime
from typing import List, Annotated, Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from src.db import conn, cur
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
def next_ticket(curr_user: Annotated[StaffSchema, Depends(auth_middleware)]):
    staff_id = str(curr_user.staff_id)
    try:
        cur.execute("""
        SELECT current_queue_number
        FROM Staff
        WHERE staff_id = %s
        """, (staff_id,))
        cqn = cur.fetchone()

        cur.execute("""
        UPDATE Queue
        SET status = 'served'
        WHERE position = %s
        """, (cqn[0],))

        cur.execute("""
        UPDATE Queue_History
        SET status = 'served'
        WHERE position = %s
        """, (cqn[0],))

        cur.execute("""
        SELECT queue_id ,MIN(position)
        FROM Queue
        WHERE status = 'on-wait'
        """)
        ticket = cur.fetchone()

        if not ticket:
            raise HTTPException(status_code=404, detail="No tickets available for assignment.")

        pos = ticket[1]
        q_id = ticket[0]

        cur.execute("""
                UPDATE Staff
                SET current_queue_number = %s
                WHERE staff_id = %s;
            """, (pos, staff_id))

        cur.execute("""
            UPDATE Queue
            SET status = 'in-progress'
            WHERE queue_id = %s;
        """, (q_id,))

        cur.execute("""
            UPDATE Queue_History
            SET status = 'in-progress'
            WHERE queue_id = %s;
        """, (q_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error assigning next ticket: {e}")
