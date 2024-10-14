import pytest

from src.main import app
from src.database import get_async_session

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

# Explicitly import all modules with sqlalchemy models, 
# so that Base.metadata contains info about all tables
from src.database import Base
import src.operations.models as operations_models
import src.auth.models as auth_models

import os
from dotenv import load_dotenv

from httpx import AsyncClient, ASGITransport

import logging

# In case you need to create a synchronous test client
# from fastapi.testclient import TestClient

# SETUP PYTEST LOGS FORMAT FOR CONSOLE
# Do not need asyncio logs of DEBUG level
logger = logging.getLogger('asyncio')
logger.setLevel(logging.INFO)

# Add new line after test name
def pytest_runtest_logstart(nodeid, location):
    print()
    pass

# Add new line after test result
def pytest_runtest_logreport(report):
    if report.when == 'call':
        print()
        pass


load_dotenv()

DB_HOST_TEST = os.environ.get("DB_HOST_TEST")
DB_PORT_TEST = os.environ.get("DB_PORT_TEST")
DB_NAME_TEST = os.environ.get("DB_NAME_TEST")
DB_USER_TEST = os.environ.get("DB_USER_TEST")
DB_PASS_TEST = os.environ.get("DB_PASS_TEST")

# DATABASE
DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

# Create engine for test, and async sessions fabric
engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)

# Binding metadata about all alchemy tables to the test engine
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session

@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# In case you need to create a synchronous test client
# client = TestClient(app)

# Сreate an asynchronous test client
@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac




