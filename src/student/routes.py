from fastapi import APIRouter

from src.student.schema import StudentSchema
from src.student.service import StudentServiceDep

student_router = APIRouter()

@student_router.post("/student/")
def create(student_serv: StudentServiceDep, student: StudentSchema) -> str:
    return student_serv.create(student)
