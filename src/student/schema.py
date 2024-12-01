from pydantic import BaseModel


class StudentSchema(BaseModel):
    student_id: str
    tg_tag: str
    notify: bool
