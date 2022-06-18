from sqlalchemy import Column, Integer, String

from backend.core.database import Base


class Mem(Base):
    id = Column(Integer, primary_key=True)
    link = Column(String, nullable=False)
