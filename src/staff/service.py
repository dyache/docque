import uuid
from datetime import datetime, timezone, timedelta
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

from src.config import Config
from src.db import cur, conn
from src.staff.models import Staff
from src.staff.repository import StaffRepository
from src.staff.schema import StaffSchema, StaffCreateSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBearer()


class StaffService:
    def __init__(self, staff_repo: StaffRepository, config: Config):
        self.staff_repo = staff_repo
        self.secret_key = config.jwt_secret_key
        self.algorithm = config.jwt_algorithm
        self.token_ttl = config.token_ttl_hours

    def hash_password(self, password: str) -> str:
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str):
        password_byte_enc = plain_password.encode('utf-8')
        return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password.encode('utf-8'))

    def authenticate_staff(self, name: str, password: str) -> bool | StaffSchema:
        staff = self.staff_repo.get_by_name(name)
        print(staff.hashed_password)
        print(staff.name)
        if not staff:
            return False
        if not self.verify_password(password, staff.hashed_password):
            return False
        staff_schema = StaffSchema(name=staff.name, staff_id=staff.staff_id)
        return staff_schema

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(hours=self.token_ttl)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_staff(self, staff: StaffCreateSchema) -> uuid.UUID:
        model_staff = Staff(staff_id=uuid.uuid4(), name=staff.name, hashed_password=self.hash_password(staff.password),
                            current_queue_number=0)
        try:
            return self.staff_repo.create(model_staff)
        except Exception as e:
            raise RuntimeError(f"error creating staff {e}")


def get_staff_service() -> StaffService:
    return StaffService(StaffRepository(conn, cur), Config())


StaffServiceDep = Annotated[StaffService, Depends(get_staff_service)]
