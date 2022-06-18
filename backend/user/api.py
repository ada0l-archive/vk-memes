from datetime import timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from backend.core import security
from backend.core.router_generator import RouterGenerator
from backend.core.settings import settings
from backend.user.dependencies import get_repository, get_current_user, get_current_active_user
from backend.user.models import User
from backend.user.repository import UserRepository
from backend.user.schemas import UserPydantic, UserInCreatePydantic, Token

router = RouterGenerator(
    prefix="/user",
    get_repository_function=get_repository,
    response_model=UserPydantic,
    pagination=10
)


@router.get("/me", response_model=UserPydantic)
async def get_me(
    user: User = Depends(get_current_active_user),
):
    return user


@router.post("/", response_model=UserPydantic)
async def create_user(
    user_in: UserInCreatePydantic,
    rep: UserRepository = Depends(get_repository),
):
    """
    Create new user.
    """
    user = await rep.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await rep.create(user_in)

    return user


@router.post("/login/access-token", response_model=Token)
async def login_access_token(
    rep: UserRepository = Depends(get_repository),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    user = await rep.authenticate(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=UserPydantic)
def test_token(current_user: UserPydantic = Depends(get_current_user)):
    """
    Test access token
    """
    return current_user
