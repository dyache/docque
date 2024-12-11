import uuid
from typing import List

from psycopg2 import IntegrityError, errors
from psycopg2.extensions import cursor, connection

from src.custom_exception import EntityAlreadyExistsException, DataException
from src.queue.exception import QueueNotFoundException
from src.queue.models import Queue


class QueueRepository:
    def __init__(self, conn: connection, cur: cursor):
        self.cursor: cursor = cur
        self.conn: connection = conn

    def create(self, queue: Queue) -> uuid.UUID:
        query = """
        INSERT INTO queue (queue_id, status, student_id ,created_at) VALUES (%s, %s, %s, %s)
        """
        try:
            self.cursor.execute(query, (queue.queue_id, queue.status, queue.student_id, queue.created_at))
            self.conn.commit()
        except IntegrityError as e:
            self.conn.rollback()
            if isinstance(e.orig, errors.UniqueViolation):
                raise EntityAlreadyExistsException("entity already exists")
            else:
                raise DataException("data error")

        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"Database error occurred: {e}")

        return queue.queue_id

    def get_by_id(self, queue_id: uuid.UUID) -> Queue:
        query = "SELECT queue_id, position, student_id, status, created_at FROM queue WHERE queue_id = %s;"
        try:
            self.cursor.execute(query, (queue_id.__str__(),))
            row = self.cursor.fetchone()
            if row:
                return Queue(queue_id=row[0], position=row[1], status=row[3], student_id=row[2], created_at=row[4])
            else:
                raise QueueNotFoundException(f"Queue item with ID '{queue_id.__str__()}' not found")
        except Exception as e:
            raise RuntimeError(f"Database error occurred: {e}")

    def get_by_position(self, position: int) -> Queue:
        query = "SELECT queue_id, position, status, created_at FROM queue WHERE position = %s;"
        try:
            self.cursor.execute(query, (position,))
            row = self.cursor.fetchone()
            if row:
                return Queue(queue_id=row[0], position=row[1], status=row[3], student_id=row[2], created_at=row[4])
            else:
                raise QueueNotFoundException(f"Queue item with position '{str(position)}' not found")
        except Exception as e:
            raise RuntimeError(f"Database error occurred: {e}")

    def get_all_sort_by_position(self) -> List[Queue]:
        query = "SELECT queue_id, position, student_id ,status, created_at FROM queue ORDER BY position;"
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            queues = [Queue(queue_id=row[0], position=row[1], status=row[3], student_id=row[2], created_at=row[4]) for
                      row in rows]
            return queues
        except Exception as e:
            raise RuntimeError(f"Database error occurred: {e}")

    def update(self, queue_id: uuid.UUID, status: str) -> bool:
        query = """
        UPDATE queue SET status = %s WHERE queue_id = %s
        """
        try:
            self.cursor.execute(query, (status, queue_id))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                raise QueueNotFoundException(f"Queue with ID {queue_id} not found")
            return True
        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"Error updating queue: {e}")
