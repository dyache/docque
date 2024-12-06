import uuid
from typing import Annotated

from fastapi import Depends
from psycopg2.extensions import cursor, connection

from src.db import cur, conn
from src.staff.exception import StaffNotFoundException
from src.staff.models import Staff


class StaffRepository:
    def __init__(self, conn: connection, cur: cursor):
        self.cursor: cursor = cur
        self.conn: connection = conn

    def create(self, staff: Staff) -> uuid.UUID:
        query = """
        INSERT INTO staff (staff_id, staff_name, hashed_password)
        VALUES (%s, %s, %s)
        """
        try:
            self.cursor.execute(query, (str(staff.staff_id), staff.name, staff.hashed_password))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"database error occurred {e}")
        return staff.staff_id

    def get_by_name(self, name: str) -> Staff:
        query = """
        SELECT staff_id, staff_name, current_queue_number, hashed_password
        FROM staff
        WHERE staff_name = %s
        """
        try:
            self.cursor.execute(query, (name,))
            result = self.cursor.fetchone()
            if result:
                print(result)
                return Staff(result[0], result[1], result[2], result[3])
            else:
                raise StaffNotFoundException(f"Staff member with name '{name}' not found")
        except Exception as e:
            raise RuntimeError(f"database error occurred {e}")

    def get_by_id(self, staff_id: uuid.UUID) -> Staff:
        query = """
        SELECT staff_id, staff_name, current_queue_number, hashed_password
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


def get_staff_repo() -> StaffRepository:
    return StaffRepository(conn, cur)


StaffRepositoryDep = Annotated[StaffRepository, Depends(get_staff_repo)]
