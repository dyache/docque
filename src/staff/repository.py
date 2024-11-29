import uuid

from psycopg2.extensions import cursor, connection

from src.staff.exception import StaffNotFoundException
from src.staff.models import Staff


class StaffRepository:
    def __init__(self, conn: connection, cur: cursor):
        self.cursor: cursor = cur
        self.conn: connection = conn

    def create(self, staff: Staff) -> uuid.UUID:
        query = """
        INSERT INTO staff (staff_id, name, current_queue_number, hashed_password)
        VALUES (%s, %s, %s, %s)
        """
        try:
            self.cursor.execute(query, (staff.staff_id, staff.name, staff.current_queue_number, staff.hashed_password))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"database error occurred {e}")
        return staff.staff_id


    def get_by_name(self, name: str) -> Staff:
        query = """
        SELECT staff_id, name, current_queue_number, hashed_password
        FROM staff
        WHERE name = %s
        """
        try:
            self.cursor.execute(query, (name,))
            result = self.cursor.fetchone()
            if result:
                return Staff(*result)
            else:
                raise StaffNotFoundException(f"Staff member with name '{name}' not found")
        except Exception as e:
            raise RuntimeError(f"database error occurred {e}")
    def get_by_id(self, staff_id: uuid.UUID) -> Staff:
        query = """
        SELECT staff_id, name, current_queue_number, hashed_password
        FROM staff
        WHERE staff_id = %s
        """
        try:
            self.cursor.execute(query, (staff_id,))
            result = self.cursor.fetchone()
            if result:
                return Staff(*result)
            else:
                raise StaffNotFoundException(f"Staff member with id '{staff_id}' not found")
        except Exception as e:
            raise RuntimeError(f"database error occurred {e}")
