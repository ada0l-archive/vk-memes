from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_session
from backend.mem.repository import MemRepository
from backend.stat.schemas import MemWithStatPydantic
from backend.user.dependencies import get_current_active_superuser
from backend.user.models import User


async def get_repository(session: AsyncSession = Depends(get_session)):
    return MemRepository(session)


router = APIRouter(tags=['stat'])


@router.get("/stat", response_model=list[MemWithStatPydantic])
async def get_stat(
    rep: MemRepository = Depends(get_repository),
    _: User = Depends(get_current_active_superuser)
):
    return await rep.get_stat()
