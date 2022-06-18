from fastapi import Query

from backend.core.schemas import PaginationPydantic


def get_pagination_filter(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, le=100)
) -> PaginationPydantic:
    return PaginationPydantic(offset=offset, limit=limit)
