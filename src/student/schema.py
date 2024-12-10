from pydantic import BaseModel


class StudentSchema(BaseModel):
    student_id: str
    notify: bool
