import uuid
from typing import List
from psycopg2.extensions import cursor, connection
from src.queue_history.model import QueueHistory

class QueueHistoryRepository:
    def __init__(self, conn: connection, cur: cursor):
        self.cursor: cursor = cur
        self.conn: connection = conn

    def create(self, queue: QueueHistory) -> uuid.UUID:
        query = """
        INSERT INTO queue_history (queue_id, status, created_at) VALUES (%s, %s, %s)
        """
        try:
            self.cursor.execute(query, (queue.queue_id, queue.status, queue.created_at))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"Database error occurred: {e}")
        return queue.queue_id

    def get_all_sort_by_created_at(self) -> List[QueueHistory]:
        query = "SELECT queue_id, position, status, created_at FROM queue ORDER BY created_at;"
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            queues = [QueueHistory(queue_id=row[0], position=row[1], created_at=row[3], status=row[2]) for row in rows]
            return queues
        except Exception as e:
            raise RuntimeError(f"Database error occurred: {e}")
