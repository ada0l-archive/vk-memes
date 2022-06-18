from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from backend.core import security
from backend.user import models, schemas
from backend.core.settings import settings

from backend.core.database import get_session
from backend.user.repository import UserRepository

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/user/login/access-token"
)


async def get_repository(session=Depends(get_session)):
    return UserRepository(session)


async def get_current_user(
    db=Depends(get_session),
    token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await UserRepository(db).get_by_id(token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
