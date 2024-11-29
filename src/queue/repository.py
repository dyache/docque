import uuid
from typing import List

from psycopg2.extensions import cursor, connection

from src.queue.exception import QueueNotFoundException
from src.queue.models import Queue


class QueueRepository:
    def __init__(self, conn: connection, cur: cursor):
        self.cursor: cursor = cur
        self.conn: connection = conn

    def create(self, queue: Queue) -> uuid.UUID:
        query = """
        INSERT INTO queue (queue_id, status, created_at) VALUES (%s, %s, %s)
        """
        try:
            self.cursor.execute(query, (queue.queue_id, queue.status, queue.created_at))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"database error occurred {e}")
        return queue.queue_id

    def get_by_id(self, queue_id: uuid.UUID) -> Queue:
        query = "SELECT queue_id, position, status, created_at FROM queue WHERE queue_id = %s;"

        try:
            self.cursor.execute(query, (queue_id.__str__()))
            result = self.cursor.fetchone()
            if result:
                return Queue(*result)
            else:
                raise QueueNotFoundException(f"queue item with id '{queue_id.__str__()}' not found")
        except Exception as e:
            raise RuntimeError(f"database error occurred {e}")

    def get_all_sort_by_position(self) -> List[Queue]:

        query = "SELECT queue_id, position, status, created_at FROM queue ORDER BY position;"

        self.cursor.execute(query)

        rows = self.cursor.fetchall()

        queues = []
        for row in rows:
            queue = Queue(queue_id=row[0], position=row[1], created_at=row[3], status=row[2])
            queues.append(queue)

        return queues
