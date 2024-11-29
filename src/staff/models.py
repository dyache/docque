import uuid


class Staff:
    def __init__(self, staff_id: uuid.UUID, name: str, hashed_password: str, current_queue_number: uuid.UUID):
        self.staff_id: uuid.UUID = staff_id
        self.name: str = name
        self.current_queue_number: uuid.UUID = current_queue_number
        self.hashed_password: str = hashed_password
