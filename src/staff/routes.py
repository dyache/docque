from fastapi import HTTPException, status, Security, APIRouter
from fastapi.security import HTTPAuthorizationCredentials

from src.staff.schema import StaffCreateSchema, Token, StaffSchema
from src.staff.service import StaffService, oauth2_scheme

staff_router = APIRouter()


class StaffRoutes:
    def __init__(self, staff_serv: StaffService):
        self.staff_serv: StaffService = staff_serv

    @staff_router.post("/staff/login")
    async def login(self, staff_schema: StaffCreateSchema):
        staff = self.staff_serv.authenticate_staff(staff_schema.name, staff_schema.password)
        if not staff:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = self.staff_serv.create_access_token(
            data={"sub": staff.staff_id}
        )
        return Token(access_token=access_token, token_type="bearer")

    @staff_router.get("/staff/me/", response_model=StaffSchema)
    async def get_me(self, auth: HTTPAuthorizationCredentials = Security(oauth2_scheme)) -> StaffSchema:
        if not auth.credentials:
            raise HTTPException(status_code=401, detail="No token provided")
        return await self.staff_serv.get_current_staff(token=auth.credentials)

    @staff_router.post("/staff")
    def register(self, staff_schema: StaffCreateSchema):
        self.staff_serv.create_staff(staff_schema)
