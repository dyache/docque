import uuid


class Staff:
    def __init__(self, staff_id: uuid.UUID, name: str, current_queue_number: int, hashed_password: str):
        self.staff_id: uuid.UUID = staff_id
        self.name: str = name
        self.current_queue_number: int = current_queue_number
        self.hashed_password: str = hashed_password
