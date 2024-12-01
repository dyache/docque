from fastapi import APIRouter

from src.student.schema import StudentSchema
from src.student.service import StudentService

student_router = APIRouter()


class StudentRoutes:
    def __init__(self, student_serv: StudentService):
        self.student_serv = student_serv

    @student_router.post("/student/")
    def create(self, student: StudentSchema) -> str:
        return self.student_serv.create(student)
