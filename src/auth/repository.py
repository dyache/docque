from sqlalchemy import Connection
class AuthRepository:
    def __init__(self, conn: Connection):
        self.conn = conn
