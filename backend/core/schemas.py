from typing import Generic, TypeVar

from pydantic import BaseModel, Field, root_validator
from pydantic.generics import GenericModel


class StatusPydantic(BaseModel):
    message: str


class PaginationPydantic(BaseModel):
    offset: int = Field(default=0)
    limit: int = Field(default=100)


DataT = TypeVar('DataT')


class ListPydantic(GenericModel, Generic[DataT]):
    items: list[DataT]
    count: int | None

    @root_validator
    def compute_count(cls, values) -> dict: # noqa
        values["count"] = len(values.get("items") if "items" in values else [])
        return values
