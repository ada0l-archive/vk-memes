from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from backend.core.database import Base
from backend.user.models import User


class Mem(Base):
    id = Column(Integer, primary_key=True)
    link = Column(String, nullable=False)


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
        UniqueConstraint('mem_id', 'user_id', name='_mem_user_uc'),
    )
