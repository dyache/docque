from typing import Annotated

from fastapi import Depends

from src.db import cur, conn
from src.student.exception import StudentAlreadyExistsException
from src.student.models import Student
from src.student.repository import StudentRepository
from src.student.schema import StudentSchema


class StudentService:
    def __init__(self, student_repo: StudentRepository):
        self.student_repo = student_repo

    def create(self, student: StudentSchema) -> str:
        student_model = Student(student_id=student.student_id, notify=student.notify)
        try:
            return self.student_repo.create(student_model)
        except RuntimeError as e:
            if "already exists in the database" in str(e):
                raise StudentAlreadyExistsException(f"Student with ID {student.student_id} already exists.") from e
            raise

def get_student_service() -> StudentService:
    return StudentService(StudentRepository(conn, cur))


StudentServiceDep = Annotated[StudentService, Depends(get_student_service)]
