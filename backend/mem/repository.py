from typing import Type

from backend.mem import schemas, models
from backend.core.repository import BaseRepository


class MemRepository(
    BaseRepository[
        models.Mem,
        schemas.MemPydantic,
        schemas.MemInCreatePydantic,
        schemas.MemInUpdatePydantic
    ]
):

    @property
    def _model(self) -> Type[models.Mem]:
        return models.Mem
