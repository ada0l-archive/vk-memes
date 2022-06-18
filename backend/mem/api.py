from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.mem.models import Mem, LikeOfMem
from backend.mem.repository import MemRepository, LikeOfMemRepository
from backend.mem.schemas import MemPydantic, LikeOfMemInCreatePydantic, LikeOfMemPydantic
from backend.core.database import get_session
from backend.core.router_generator import RouterGenerator
from backend.user.dependencies import get_current_active_user
from backend.user.models import User


async def get_repository(session: AsyncSession = Depends(get_session)):
    return MemRepository(session)


async def get_like_repository(session: AsyncSession = Depends(get_session)):
    return LikeOfMemRepository(session)


router = RouterGenerator(
    prefix="/mem",
    get_repository_function=get_repository,
    response_model=MemPydantic,
    pagination=10
)


@router.get("/", response_model=MemPydantic)
async def get_next(
    rep: MemRepository = Depends(get_repository),
    user: User = Depends(get_current_active_user)
):
    return await rep.get_next_for_user(user)


@router.post("/{item_id}/like", response_model=LikeOfMemPydantic)
async def like_mem(
    item_id: int,
    rep: MemRepository = Depends(get_repository),
    like_rep: LikeOfMemRepository = Depends(get_like_repository),
    user: User = Depends(get_current_active_user)
):
    mem = await rep.get_by_id(item_id)
    if not mem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    like = await like_rep.get(item_id, user.id)
    if like:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Already liked')
    return await like_rep.create(LikeOfMemInCreatePydantic(
        mem_id=item_id,
        user_id=user.id
    ))
