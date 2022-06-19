from backend.mem.schemas import MemPydantic


class MemWithStatPydantic(MemPydantic):
    likes_count: int
    skips_count: int
