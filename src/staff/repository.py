import uuid
from typing import Annotated, List, Dict, Any

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
            self.cursor.execute(query, (str(staff_id),))
            result = self.cursor.fetchone()
            if result:
                print(result)
                return Staff(result[0], result[1], result[2], result[3])
            else:
                raise StaffNotFoundException(f"Staff member with id '{staff_id}' not found")
        except Exception as e:
            raise RuntimeError(f"database error occurred {e}")

    def get_all(self) -> List[Staff]:
        query = """
        SELECT staff_id, staff_name, current_queue_number, hashed_password
        FROM staff
        """
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return [Staff(staff_id=row[0], name=row[1], current_queue_number=row[2], hashed_password=row[3]) for row in
                    result]
        except Exception as e:
            raise RuntimeError(f"database error occurred {e}")

    def delete(self, staff_id: uuid.UUID) -> bool:
        query = """
        DELETE FROM staff WHERE staff_id = %s
        """
        try:
            self.cursor.execute(query, (str(staff_id),))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"database error occurred {e}")

    def update(self, staff: Staff) -> bool:
        query = """
        UPDATE staff SET staff_name = %s, hashed_password = %s, current_queue_number = %s
        WHERE staff_id = %s
        """
        try:
            self.cursor.execute(query,
                                (staff.name, staff.hashed_password, staff.current_queue_number, str(staff.staff_id)))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"database error occurred {e}")

    def get_staff_with_queue(self) -> List[Dict[str, Any]]:
        query = """
        SELECT staff_id, staff_name, queue_id, position, status
        FROM staff_with_queue
        """
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return [
                {
                    "staff_id": row[0],
                    "staff_name": row[1],
                    "queue_id": row[2],
                    "position": row[3],
                    "status": row[4]
                } for row in result
            ]
        except Exception as e:
            raise RuntimeError(f"database error occurred {e}")

    def get_queue_with_staff_info(self) -> List[Dict[str, Any]]:
        query = """
        SELECT queue_id, position, status, staff_name, staff_id
        FROM queue_with_staff_info
        """
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return [
                {
                    "queue_id": row[0],
                    "position": row[1],
                    "status": row[2],
                    "staff_name": row[3],
                    "staff_id": row[4]
                } for row in result
            ]
        except Exception as e:
            raise RuntimeError(f"database error occurred {e}")


def get_staff_repo() -> StaffRepository:
    return StaffRepository(conn, cur)


StaffRepositoryDep = Annotated[StaffRepository, Depends(get_staff_repo)]
