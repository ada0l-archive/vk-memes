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
