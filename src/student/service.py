from src.student.models import Student
from src.student.repository import StudentRepository
from src.student.schema import StudentSchema
from src.db import cur, conn
from fastapi import Depends
from typing import Annotated

class StudentService:
    def __init__(self, student_repo: StudentRepository):
        self.student_repo = student_repo

    def create(self, student: StudentSchema) -> str:
        student_model = Student(student_id=student.student_id, tg_tag=student.tg_tag, notify=student.notify)
        return self.student_repo.create(student_model)

def get_student_service() -> StudentService:
    return StudentService(StudentRepository(conn,cur))
StudentServiceDep = Annotated[StudentService,Depends(get_student_service)]