import asyncio

import pytest

from backend.core.database import init_db, get_session

DB_URL = "sqlite://:memory:"


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(autouse=True)
async def initialize_tests():
    await init_db()
    yield


@pytest.fixture(scope="session")
def session():
    return get_session()
