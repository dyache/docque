from psycopg2.extensions import cursor, connection
from psycopg2.errors import UniqueViolation

from src.student.models import Student




class StudentRepository:
    def __init__(self, conn: connection, cur: cursor):
        self.cursor: cursor = cur
        self.conn: connection = conn

    def create(self, student: Student) -> str:
        query = """
        INSERT INTO "student" (student_id, notify)
        VALUES (%s, %s)
        """
        try:
            self.cursor.execute(query, (student.student_id, student.notify))
            self.conn.commit()
        except UniqueViolation:
            self.conn.rollback()
            raise RuntimeError(f"Student with ID {student.student_id} already exists in the database.")
        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"Database error occurred: {e}")
        return student.student_id

