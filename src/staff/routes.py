from fastapi import HTTPException, status, Security, APIRouter
from fastapi.security import HTTPAuthorizationCredentials

from src.staff.schema import StaffCreateSchema, Token, StaffSchema
from src.staff.service import StaffServiceDep, oauth2_scheme

staff_router = APIRouter()


@staff_router.post("/login")
async def login(staff_serv: StaffServiceDep, staff_schema: StaffCreateSchema,
                ):
    try:
        staff = staff_serv.authenticate_staff(staff_schema.name, staff_schema.password)
        if not staff:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = staff_serv.create_access_token(
            data={"sub": str(staff.staff_id)}
        )
        return Token(access_token=access_token, token_type="bearer")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from exc


@staff_router.get("/me/", response_model=StaffSchema)
async def get_me(staff_serv: StaffServiceDep,
                 auth: HTTPAuthorizationCredentials = Security(oauth2_scheme)) -> StaffSchema:
    try:
        if not auth.credentials:
            raise HTTPException(status_code=401, detail="No token provided")
        return await staff_serv.get_current_staff(token=auth.credentials)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from exc


@staff_router.post("/")
def register(staff_serv: StaffServiceDep, staff_schema: StaffCreateSchema):
    try:
        staff_serv.create_staff(staff_schema)
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from exc
