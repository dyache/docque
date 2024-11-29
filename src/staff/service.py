import uuid
from datetime import datetime, timezone, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext

from src.config import Config
from src.staff.models import Staff
from src.staff.repository import StaffRepository
from src.staff.schema import StaffSchema, TokenData, StaffCreateSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBearer()


class StaffService:
    def __init__(self, staff_repo: StaffRepository, pwd_ctx: CryptContext, config: Config):
        self.staff_repo = staff_repo
        self.pwd_ctx = pwd_ctx
        self.secret_key = config.jwt_secret_key
        self.algorithm = config.jwt_algorithm
        self.token_ttl = config.token_ttl_hours

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_ctx.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_ctx.hash(password)

    def authenticate_staff(self, name: str, password: str) -> bool | StaffSchema:
        staff = self.staff_repo.get_by_name(name)
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

    async def get_current_staff(self, token: Annotated[str, Depends(oauth2_scheme)]) -> StaffSchema:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            staff_id: uuid.UUID = payload.get("sub")
            if staff_id is None:
                raise credentials_exception
            token_data = TokenData(staff_id=staff_id)
        except InvalidTokenError:
            raise credentials_exception
        staff = self.staff_repo.get_by_id(token_data.staff_id)
        if staff is None:
            raise credentials_exception
        staff_schema = StaffSchema(name=staff.name, staff_id=staff.staff_id)
        return staff_schema

    def create_staff(self, staff: StaffCreateSchema) -> uuid.UUID:
        model_staff = Staff(uuid.uuid4(), staff.name, self.get_password_hash(staff.password))
        try:
            return self.staff_repo.create(model_staff)
        except Exception as e:
            raise RuntimeError(f"error creating staff {e}")
