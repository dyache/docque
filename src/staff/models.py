import uuid


class Staff:
    def __init__(self, staff_id: uuid.UUID, name: str, hashed_password: bytes, current_queue_number: int):
        self.staff_id: uuid.UUID = staff_id
        self.name: str = name
        self.current_queue_number: int = current_queue_number
        self.hashed_password: bytes = hashed_password
