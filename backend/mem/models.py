from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, select, func
from sqlalchemy.orm import relationship, object_session, query_expression

from backend.core.database import Base
from backend.user.models import User


class Mem(Base):
    id = Column(Integer, primary_key=True)
    link = Column(String, nullable=False)

    likes_count = query_expression()
    skips_count = query_expression()

    # @property
    # def likes_count(self):
    #     return object_session(self).\
    #         scalar(
    #             select(func.count(LikeOfMem.id)).
    #             where(LikeOfMem.mem_id == id)
    #         )


class LikeOfMem(Base):
    id = Column(Integer, primary_key=True)
    mem_id = Column(Integer, ForeignKey(Mem.id, ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))
    __table_args__ = (
        UniqueConstraint('mem_id', 'user_id', name='_mem_user_uc'),
    )


class SkipOfMem(Base):
    id = Column(Integer, primary_key=True)
    mem_id = Column(Integer, ForeignKey(Mem.id, ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))
    __table_args__ = (
        UniqueConstraint('mem_id', 'user_id', name='_mem_user_skip_uc'),
    )
