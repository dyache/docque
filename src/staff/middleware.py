import uuid
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status, Header
from jwt import InvalidTokenError

from src.db import settings
from src.staff.repository import StaffRepositoryDep
from src.staff.schema import StaffSchema, TokenData
from src.staff.service import oauth2_scheme


async def auth_middleware(token: Annotated[str, Depends(oauth2_scheme)], staff_repo: StaffRepositoryDep,
                          tg_api_key: Annotated[str | None, Header()] = None) -> StaffSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if tg_api_key == settings.tg_bot_api_key:
        return StaffSchema(name="tg")
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        staff_id: uuid.UUID = payload.get("sub")
        if staff_id is None:
            raise credentials_exception
        token_data = TokenData(staff_id=staff_id)
    except InvalidTokenError:
        raise credentials_exception
    staff = staff_repo.get_by_id(token_data.staff_id)
    if staff is None:
        raise credentials_exception
    staff_schema = StaffSchema(name=staff.name, staff_id=staff.staff_id)
    return staff_schema
