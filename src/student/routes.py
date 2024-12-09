from typing import Annotated

from fastapi import APIRouter, Depends

from src.staff.middleware import auth_middleware
from src.staff.schema import StaffSchema
from src.student.schema import StudentSchema
from src.student.service import StudentServiceDep

student_router = APIRouter()


@student_router.post("/")
async def create(student_serv: StudentServiceDep, student: StudentSchema,
                 curr_user: Annotated[StaffSchema, Depends(auth_middleware)]) -> str:
    return student_serv.create(student)
