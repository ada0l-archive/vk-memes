from typing import Type

from backend.core.security import get_password_hash, verify_password
from backend.user import schemas, models
from backend.core.repository import BaseRepository


class UserRepository(
    BaseRepository[
        models.User,
        schemas.UserPydantic,
        schemas.UserInCreatePydantic,
        schemas.UserInUpdatePydantic
    ]
):

    @property
    def _model(self) -> Type[models.User]:
        return models.User

    async def get_by_email(self, email: str):
        q = await self.session.execute(self.get_query().filter(self._model.email == email))
        return q.scalars().first()

    async def create(self, schema_in: schemas.UserInCreatePydantic, commit: bool = True):
        schema_in_dict = schema_in.dict()
        schema_in_dict['hashed_password'] = get_password_hash(schema_in_dict['password'])
        del schema_in_dict['password']
        db_obj = self._model(**schema_in_dict)  # noqa
        self.session.add(db_obj)
        if commit:
            await self.session.commit()
            await self.session.refresh(db_obj)
        return db_obj

    async def authenticate(self, email: str, password: str) -> models.User | None:
        user = await self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
