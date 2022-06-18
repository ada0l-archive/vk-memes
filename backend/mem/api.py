from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.mem.repository import MemRepository
from backend.mem.schemas import MemPydantic
from backend.core.database import get_session
from backend.core.router_generator import RouterGenerator


async def get_repository(session: AsyncSession = Depends(get_session)):
    return MemRepository(session)


router = RouterGenerator(
    prefix="/mem",
    get_repository_function=get_repository,
    response_model=MemPydantic,
    pagination=10
)