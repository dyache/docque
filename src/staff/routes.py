from typing import Annotated, List, Dict, Any
from uuid import UUID

from fastapi import HTTPException, status, APIRouter, Depends

from src.staff.exception import StaffNotFoundException
from src.staff.middleware import auth_middleware
from src.staff.models import Staff
from src.staff.schema import StaffCreateSchema, Token, StaffSchema, StaffUpdateSchema
from src.staff.service import StaffServiceDep

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
async def get_me(
        curr_user: Annotated[StaffSchema, Depends(auth_middleware)]
) -> StaffSchema:
    return curr_user


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


@staff_router.get("/", response_model=List[StaffSchema])
def get_all_staff(
        staff_serv: StaffServiceDep,
        curr_user: Annotated[StaffSchema, Depends(auth_middleware)]
):
    try:
        return staff_serv.staff_repo.get_all()
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch staff members",
        ) from exc


@staff_router.get("/{staff_id}", response_model=StaffSchema)
def get_staff_by_id(
        staff_id: UUID,
        staff_serv: StaffServiceDep,
        curr_user: Annotated[StaffSchema, Depends(auth_middleware)]
):
    try:
        return staff_serv.staff_repo.get_by_id(staff_id)
    except StaffNotFoundException as not_found_exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(not_found_exc),
        )
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving staff member",
        ) from exc


@staff_router.put("/", response_model=bool)
def update_staff(
        staff_serv: StaffServiceDep,
        staff_schema: StaffUpdateSchema,
        curr_user: Annotated[StaffSchema, Depends(auth_middleware)]
):
    try:
        staff_model = Staff(
            staff_id=staff_schema.staff_id,
            name=staff_schema.name,
            hashed_password=staff_serv.hash_password(staff_schema.password),
            current_queue_number=staff_schema.current_queue_number,
        )
        return staff_serv.staff_repo.update(staff_model)
    except StaffNotFoundException as not_found_exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(not_found_exc),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating staff member",
        ) from exc


@staff_router.delete("/{staff_id}", response_model=bool)
def delete_staff(
        staff_id: UUID,
        staff_serv: StaffServiceDep,
        curr_user: Annotated[StaffSchema, Depends(auth_middleware)]
):
    try:
        return staff_serv.staff_repo.delete(staff_id)
    except StaffNotFoundException as not_found_exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(not_found_exc),
        )
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting staff member",
        ) from exc


@staff_router.get("/queue", response_model=List[dict])
def get_staff_with_queue(staff_serv: StaffServiceDep):
    try:
        return staff_serv.get_staff_with_queue()
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from exc


@staff_router.get("/queue/staff-info", response_model=List[Dict[str, Any]])
def get_queue_with_staff_info(staff_serv: StaffServiceDep):
    try:
        return staff_serv.get_queue_with_staff_info()
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from exc
