from pydantic import BaseModel


class MemBasePydantic(BaseModel):
    link: str


class MemPydantic(MemBasePydantic):
    id: int

    class Config:
        orm_mode = True


class MemInCreatePydantic(MemBasePydantic):
    pass


class MemInUpdatePydantic(MemBasePydantic):
    pass


class LikeOfMemBasePydantic(BaseModel):
    user_id: int
    mem_id: int


class LikeOfMemPydantic(LikeOfMemBasePydantic):
    id: int

    class Config:
        orm_mode = True


class LikeOfMemInCreatePydantic(LikeOfMemBasePydantic):
    pass


class LikeOfMemInUpdatePydantic(BaseModel):
    pass


class SkipOfMemBasePydantic(BaseModel):
    user_id: int
    mem_id: int


class SkipOfMemPydantic(LikeOfMemBasePydantic):
    id: int

    class Config:
        orm_mode = True


class SkipOfMemInCreatePydantic(LikeOfMemBasePydantic):
    pass


class SkipOfMemInUpdatePydantic(BaseModel):
    pass
