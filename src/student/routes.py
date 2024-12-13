from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.staff.middleware import auth_middleware
from src.staff.schema import StaffSchema
from src.student.exception import StudentAlreadyExistsException
from src.student.schema import StudentSchema
from src.student.service import StudentServiceDep

student_router = APIRouter()


@student_router.post("/")
async def create(
        student_serv: StudentServiceDep,
        student: StudentSchema,
        curr_user: Annotated[StaffSchema, Depends(auth_middleware)],
) -> str:
    try:
        return student_serv.create(student)
    except StudentAlreadyExistsException as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        ) from e
