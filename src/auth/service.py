from passlib.context import CryptContext

from src.auth.repository import AuthRepository


class AuthService:
    def __init__(self, auth_repo: AuthRepository, pwd_ctx: CryptContext):
        self.auth_repo: AuthRepository = auth_repo
        self.pwd_ctx: CryptContext = pwd_ctx

    def verify_password(self,plain_password: str, hashed_password:str) -> bool:
        return self.pwd_ctx.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_ctx.hash(password)