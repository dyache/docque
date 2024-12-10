from typing import Annotated

from fastapi import APIRouter, Depends, Request

from src.staff.middleware import auth_middleware
from src.staff.schema import StaffSchema
from src.student.schema import StudentSchema
from src.student.service import StudentServiceDep

student_router = APIRouter()


@student_router.post("/")
async def create(student_serv: StudentServiceDep, request: Request, student: StudentSchema,
                 curr_user: Annotated[StaffSchema, Depends(auth_middleware)]) -> str:
    body = await request.body()
    print(body)
    return student_serv.create(student)
