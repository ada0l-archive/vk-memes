from pydantic import BaseModel, EmailStr


class UserBasePydantic(BaseModel):
    full_name: str
    email: EmailStr


class UserPydantic(UserBasePydantic):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class UserInCreatePydantic(UserBasePydantic):
    password: str


class UserInUpdatePydantic(UserBasePydantic):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: int | None = None
