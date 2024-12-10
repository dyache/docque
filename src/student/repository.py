from psycopg2.extensions import cursor, connection

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
        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"database error occurred {e}")
        return student.student_id
