---
name: python-testing
description: "Write or modify Python tests. Use when: adding new tests, understanding testing conventions, working with fixtures, writing FastAPI route tests, database tests, or following pytest patterns. DO NOT USE FOR RUNNING TESTS. If you are just running tests, not building them, you do not need this."
---

# Python Testing

> **context7**: If the `context7_query-docs` tool is available, resolve and load the full `pytest` documentation before creating new tests or running pytest commands not in the makefile:
> ```
> context7_resolve-library-id: "pytest"
> context7_query-docs: /pytest-dev/pytest "<query>"
> ```

Guidelines and patterns for writing tests in this codebase.

---

## General Rules

- **No test classes** unless there is a specific technical reason. Prefer standalone functions.
- **All fixtures** must be defined or imported in `conftest.py` so they are automatically available to all tests in that directory.
- **No mocks for simple dataclasses or Pydantic models** — construct an instance directly with the desired parameters instead.
- **Test file structure mirrors the main code** — a test for `{{cookiecutter.__package_slug}}/foo.py` lives at `tests/test_foo.py`.
- **When adding new code, add tests to cover it.**

---

## Running Tests

```bash
make pytest              # Run full test suite with coverage report
make pytest_loud         # Run with debug logging enabled
uv run pytest            # Run directly — append any pytest options/arguments
uv run pytest tests/test_foo.py -k test_my_function -s
```

---

{%- if cookiecutter.include_fastapi == "y" %}

## FastAPI Tests

Use the FastAPI `TestClient` via a fixture rather than calling router classes directly.

```python
import pytest
from fastapi.testclient import TestClient
from {{cookiecutter.__package_slug}}.www import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_get_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
```

---

{%- endif %}

{%- if cookiecutter.include_sqlalchemy == "y" %}

## Database Tests

Use a memory-backed SQLite fixture. Wire it into the FastAPI app via a dependency override so routes use the test database automatically.

```python
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from {{cookiecutter.__package_slug}}.models.base import Base


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

    await engine.dispose()
```

---

{%- endif %}

## Fixture Conventions

- Fixtures shared across multiple test files → `tests/conftest.py`
- Fixtures specific to a subdirectory → `tests/<subdirectory>/conftest.py`
- Complex fixture content → `tests/fixtures/`

---

## Style Checklist

- [ ] Test is a standalone function (no wrapping class)
- [ ] Fixtures defined/imported in `conftest.py`
- [ ] No mocks for dataclasses or Pydantic models — use real instances
{%- if cookiecutter.include_sqlalchemy == "y" %}
- [ ] Database tests use memory SQLite with dependency override
{%- endif %}
{%- if cookiecutter.include_fastapi == "y" %}
- [ ] FastAPI tests use `TestClient` fixture
{%- endif %}
- [ ] Test file location mirrors the module being tested

---

## Further Reading

- [docs/dev/testing.md](../../docs/dev/testing.md) — Full testing developer guide covering pytest configuration, coverage reporting, async test patterns, database test fixtures, and CI integration.
- [pytest Docs](https://docs.pytest.org/)
- [pytest-asyncio Docs](https://pytest-asyncio.readthedocs.io/)
