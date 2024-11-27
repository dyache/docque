from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext

import jwt

from src.auth.models import User
from src.auth.repository import AuthRepository
from src.auth.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthService:
    def __init__(self, auth_repo: AuthRepository, pwd_ctx: CryptContext):
        self.auth_repo: AuthRepository = auth_repo
        self.pwd_ctx: CryptContext = pwd_ctx

    def verify_password(self,plain_password: str, hashed_password:str) -> bool:
        return self.pwd_ctx.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_ctx.hash(password)

    def authenticate_user(self, name: str, password: str) -> bool | User:
        user = self.auth_repo.get_user_by_name(name)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        user = self.auth_repo.get_user_by_name(token_data.username)
        if user is None:
            raise credentials_exception
        return user

    async def get_current_active_user(
            self,
            current_user: Annotated[User, Depends(get_current_user)],
    ):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

