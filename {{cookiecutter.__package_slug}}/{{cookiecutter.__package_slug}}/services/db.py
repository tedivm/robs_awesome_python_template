from contextlib import asynccontextmanager
import os
from typing import AsyncGenerator
from urllib.parse import urlparse


from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from ..settings import settings

# SQLAlchemy async engine requires non-standard driver DSN that don't work with other libraries.
# We use the standard but transform it for the async engine.
engine_mappings = {
    "sqlite": "sqlite+aiosqlite",
    "postgresql": "postgresql+asyncpg",
}

db_url = settings.database_url
for find, replace in engine_mappings.items():
    db_url = db_url.replace(find, replace)


engine = create_async_engine(db_url, future=True, echo=settings.debug)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


{%- if cookiecutter.include_fastapi == "y" %}
async def get_session_depends() -> AsyncGenerator[AsyncSession, None]:
    async with get_session() as session:
        yield session
{%- endif %}

async def test_data(session: AsyncSession) -> None:
    """Populate the test database with initial data."""
    if os.environ.get("IS_DEV", "") != "":
        raise ValueError("This function should not be called in production. Enable IS_DEV to run it in development.")

    # Example: Add initial data to the session
    # await session.add_all([YourModel(name="Test")])
    # await session.commit()

