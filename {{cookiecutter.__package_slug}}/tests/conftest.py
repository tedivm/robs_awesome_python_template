import pytest_asyncio


{%- if cookiecutter.include_sqlalchemy == "y" %}
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from {{cookiecutter.__package_slug}}.models.base import Base
from {{cookiecutter.__package_slug}}.services.db import get_session_depends, test_data
{%- endif %}

{%- if cookiecutter.include_fastapi == "y" %}
from fastapi.testclient import TestClient
from {{cookiecutter.__package_slug}}.www import app
{%- endif %}

{%- if cookiecutter.include_sqlalchemy == "y" %}

@pytest_asyncio.fixture
async def db_session_maker(tmpdir):
    """Creates a test database engine, complete with fake data."""
    test_database_url = f"sqlite+aiosqlite:///{tmpdir}/test_database.db"  # Use SQLite for testing; adjust as needed
    engine = create_async_engine(test_database_url, future=True, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session_maker() as session:
        await test_data(session)

    yield async_session_maker

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_session_maker):
    async with db_session_maker() as session:
        yield session

{%- endif %}

{%- if cookiecutter.include_fastapi == "y" %}
@pytest_asyncio.fixture
{%- if cookiecutter.include_sqlalchemy == "y" %}
async def fastapi_client(db_session_maker):
{% else %}
async def fastapi_client():
{%- endif %}

    """Fixture to create a FastAPI test client."""
    client = TestClient(app)

{%- if cookiecutter.include_sqlalchemy == "y" %}

    async def get_session_depends_override():
        async with db_session_maker() as session:
            yield session

    app.dependency_overrides[get_session_depends] = get_session_depends_override
{%- endif %}
    yield client
{%- endif %}
