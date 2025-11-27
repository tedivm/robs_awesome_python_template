# Testing

This project uses [pytest](https://docs.pytest.org/) as its testing framework, providing comprehensive test coverage for all features with async/await support, fixtures, and powerful assertion capabilities.

## Project Test Structure

Tests are organized in the `tests/` directory with a structure that mirrors the main package:

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures and test configuration
├── test_cli.py              # CLI application tests
├── test_celery.py           # Celery task queue tests
├── test_qq.py               # QuasiQueue multiprocessing tests
├── test_settings.py         # Settings and configuration tests
├── test_www.py              # FastAPI web application tests
└── services/
    ├── __init__.py
    ├── test_cache.py        # Cache service tests
    └── test_jinja.py        # Template service tests
```

### Test Organization Principles

- **Mirror package structure**: Test files mirror the structure of the main package
- **Feature-based testing**: Each major feature has its own test file
- **Shared fixtures**: Common test setup is centralized in `conftest.py`

## Running Tests

### Basic Test Execution

```bash
# Run all tests
make test

# Run only pytest (skip linting and type checks)
make pytest

# Run tests with verbose output
make pytest_loud

# Run specific test file
pytest tests/test_www.py

# Run specific test function
pytest tests/test_www.py::test_root_redirects_to_docs

# Run tests matching a pattern
pytest -k "test_cache"
```

### Coverage Reports

The project is configured to generate test coverage reports automatically:

```bash
# Run tests with coverage (default for make pytest)
pytest --cov=./{{cookiecutter.__package_slug}} --cov-report=term-missing tests

# Generate HTML coverage report
pytest --cov=./{{cookiecutter.__package_slug}} --cov-report=html tests
# Open htmlcov/index.html in your browser

# Show coverage for specific file
pytest --cov=./{{cookiecutter.__package_slug}}/services/cache.py tests/services/test_cache.py
```

### Running Specific Test Types

```bash
# Run only async tests
pytest -m asyncio

# Run tests in parallel (requires pytest-xdist)
pytest -n auto

# Stop on first failure
pytest -x

# Show local variables in tracebacks
pytest -l

# Disable captured output (see prints immediately)
pytest -s
```

## Test Fixtures

Test fixtures provide reusable test setup and teardown logic. This project uses fixtures extensively for database sessions, API clients, and other shared resources.

### Core Fixtures (in conftest.py)

{%- if cookiecutter.include_sqlalchemy == "y" %}

#### Database Fixtures

**db_session_maker**

Creates an in-memory SQLite database for testing, complete with all tables and test data:

```python
@pytest_asyncio.fixture
async def db_session_maker(tmpdir):
    """Creates a test database engine, complete with fake data."""
    test_database_url = f"sqlite+aiosqlite:///{tmpdir}/test_database.db"
    engine = create_async_engine(test_database_url, future=True, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session_maker() as session:
        await test_data(session)

    yield async_session_maker

    await engine.dispose()
```

**db_session**

Provides a single database session for tests:

```python
@pytest_asyncio.fixture
async def db_session(db_session_maker):
    async with db_session_maker() as session:
        yield session
```

**Usage Example:**

```python
@pytest.mark.asyncio
async def test_create_user(db_session):
    """Test creating a user in the database."""
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    await db_session.commit()

    # Query to verify
    result = await db_session.execute(select(User).where(User.email == "test@example.com"))
    saved_user = result.scalar_one()
    assert saved_user.name == "Test User"
```

{%- endif %}

{%- if cookiecutter.include_fastapi == "y" %}

#### FastAPI Fixtures

**fastapi_client**

Provides a test client for making HTTP requests to your FastAPI application:

```python
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
```

**Usage Example:**

```python
def test_api_endpoint(fastapi_client):
    """Test API endpoint returns correct data."""
    response = fastapi_client.get("/api/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
```

{%- endif %}

{%- if cookiecutter.include_cli == "y" %}

#### CLI Fixtures

**runner**

Provides a Typer CLI test runner for invoking CLI commands:

```python
from typer.testing import CliRunner
from {{cookiecutter.__package_slug}}.cli import app

runner = CliRunner()
```

**Usage Example:**

```python
def test_version_command():
    """Test that version command executes successfully."""
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "{{cookiecutter.__package_slug}}" in result.stdout
```

{%- endif %}

## Testing Async Code

This project extensively uses async/await. pytest-asyncio provides support for testing async functions.

### Async Test Functions

Mark async test functions with `@pytest.mark.asyncio`:

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """Test an async function."""
    result = await some_async_function()
    assert result == expected_value
```

### Async Fixtures

Use `@pytest_asyncio.fixture` for async fixtures:

```python
import pytest_asyncio

@pytest_asyncio.fixture
async def async_resource():
    """Create an async resource for testing."""
    resource = await create_resource()
    yield resource
    await cleanup_resource(resource)
```

### Testing Async Context Managers

```python
@pytest.mark.asyncio
async def test_async_context_manager():
    """Test async context manager."""
    async with get_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        assert len(users) >= 0
```

## Mocking and Patching

Use pytest's built-in mocking capabilities along with unittest.mock for mocking dependencies.

### Basic Mocking

```python
from unittest.mock import AsyncMock, MagicMock, patch

@pytest.mark.asyncio
async def test_with_mock():
    """Test with a mocked dependency."""
    mock_service = AsyncMock()
    mock_service.get_data.return_value = {"key": "value"}

    result = await function_using_service(mock_service)
    assert result["key"] == "value"
    mock_service.get_data.assert_called_once()
```

### Patching Functions

```python
@pytest.mark.asyncio
@patch('{{cookiecutter.__package_slug}}.services.cache.get_cached')
async def test_with_patched_cache(mock_get_cached):
    """Test with patched cache function."""
    mock_get_cached.return_value = "cached_value"

    result = await function_using_cache("key")
    assert result == "cached_value"
    mock_get_cached.assert_called_with("key")
```

### Patching Environment Variables

```python
@pytest.mark.asyncio
@patch.dict(os.environ, {"DATABASE_URL": "sqlite+aiosqlite:///:memory:"})
async def test_with_custom_env():
    """Test with custom environment variables."""
    from {{cookiecutter.__package_slug}}.settings import settings
    settings.reload()  # Reload settings with new env vars
    assert settings.database_url == "sqlite+aiosqlite:///:memory:"
```

## Testing Patterns by Feature

{%- if cookiecutter.include_fastapi == "y" %}

### Testing FastAPI Endpoints

```python
def test_get_endpoint(fastapi_client):
    """Test GET endpoint."""
    response = fastapi_client.get("/api/resource")
    assert response.status_code == 200

def test_post_endpoint(fastapi_client):
    """Test POST endpoint with JSON body."""
    data = {"name": "Test", "value": 42}
    response = fastapi_client.post("/api/resource", json=data)
    assert response.status_code == 201
    assert response.json()["name"] == "Test"

def test_endpoint_validation(fastapi_client):
    """Test endpoint validates input."""
    invalid_data = {"invalid": "data"}
    response = fastapi_client.post("/api/resource", json=invalid_data)
    assert response.status_code == 422  # Unprocessable Entity
```

### Testing OpenAPI Documentation

```python
def test_openapi_schema(fastapi_client):
    """Test that OpenAPI schema is accessible."""
    response = fastapi_client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "paths" in schema
```

{%- endif %}

{%- if cookiecutter.include_sqlalchemy == "y" %}

### Testing Database Operations

```python
@pytest.mark.asyncio
async def test_create_record(db_session):
    """Test creating a database record."""
    record = MyModel(name="Test", value=123)
    db_session.add(record)
    await db_session.commit()

    # Refresh to get ID
    await db_session.refresh(record)
    assert record.id is not None

@pytest.mark.asyncio
async def test_query_records(db_session):
    """Test querying database records."""
    result = await db_session.execute(select(MyModel).where(MyModel.name == "Test"))
    record = result.scalar_one_or_none()
    assert record is not None

@pytest.mark.asyncio
async def test_update_record(db_session):
    """Test updating a database record."""
    result = await db_session.execute(select(MyModel).where(MyModel.name == "Test"))
    record = result.scalar_one()

    record.value = 456
    await db_session.commit()

    # Verify update
    await db_session.refresh(record)
    assert record.value == 456

@pytest.mark.asyncio
async def test_delete_record(db_session):
    """Test deleting a database record."""
    result = await db_session.execute(select(MyModel).where(MyModel.name == "Test"))
    record = result.scalar_one()

    await db_session.delete(record)
    await db_session.commit()

    # Verify deletion
    result = await db_session.execute(select(MyModel).where(MyModel.name == "Test"))
    assert result.scalar_one_or_none() is None
```

### Testing with Transaction Rollback

```python
@pytest.mark.asyncio
async def test_with_rollback(db_session):
    """Test operation with rollback."""
    record = MyModel(name="Test Rollback")
    db_session.add(record)
    await db_session.flush()  # Get ID without committing

    # Verify it exists in current transaction
    result = await db_session.execute(select(MyModel).where(MyModel.name == "Test Rollback"))
    assert result.scalar_one_or_none() is not None

    await db_session.rollback()

    # Verify it's gone after rollback
    result = await db_session.execute(select(MyModel).where(MyModel.name == "Test Rollback"))
    assert result.scalar_one_or_none() is None
```

{%- endif %}

{%- if cookiecutter.include_cli == "y" %}

### Testing CLI Commands

```python
from typer.testing import CliRunner
from {{cookiecutter.__package_slug}}.cli import app

runner = CliRunner()

def test_cli_command():
    """Test CLI command execution."""
    result = runner.invoke(app, ["command", "--arg", "value"])
    assert result.exit_code == 0
    assert "Expected output" in result.stdout

def test_cli_command_with_error():
    """Test CLI command error handling."""
    result = runner.invoke(app, ["command", "--invalid"])
    assert result.exit_code != 0
    assert "Error" in result.stdout

def test_cli_help():
    """Test CLI help output."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.stdout
```

{%- endif %}

{%- if cookiecutter.include_aiocache == "y" %}

### Testing Cache Operations

```python
@pytest.mark.asyncio
async def test_cache_set_and_get():
    """Test setting and getting cached values."""
    from {{cookiecutter.__package_slug}}.services.cache import set_cached, get_cached

    await set_cached("test_key", "test_value")
    result = await get_cached("test_key")
    assert result == "test_value"

@pytest.mark.asyncio
async def test_cache_with_ttl():
    """Test cache with TTL."""
    import asyncio
    from {{cookiecutter.__package_slug}}.services.cache import set_cached, get_cached

    await set_cached("ttl_key", "ttl_value", ttl=1)
    result = await get_cached("ttl_key")
    assert result == "ttl_value"

    # Wait for expiration
    await asyncio.sleep(2)
    result = await get_cached("ttl_key")
    assert result is None

@pytest.mark.asyncio
async def test_cache_disabled():
    """Test cache operations when caching is disabled."""
    import os
    from unittest.mock import patch
    from {{cookiecutter.__package_slug}}.services.cache import set_cached, get_cached

    with patch.dict(os.environ, {"CACHE_ENABLED": "False"}):
        await set_cached("disabled_key", "disabled_value")
        result = await get_cached("disabled_key")
        # When caching is disabled, get returns None
        assert result is None
```

{%- endif %}

{%- if cookiecutter.include_celery == "y" %}

### Testing Celery Tasks

```python
def test_celery_task_registration():
    """Test that task is registered with Celery."""
    from {{cookiecutter.__package_slug}}.celery import celery, my_task

    assert "{{cookiecutter.__package_slug}}.celery.my_task" in celery.tasks

def test_celery_task_execution():
    """Test direct task execution."""
    from {{cookiecutter.__package_slug}}.celery import my_task

    # Execute task directly (not async via worker)
    result = my_task("test_arg")
    assert result == expected_value

def test_celery_task_signature():
    """Test task signature and delay methods."""
    from {{cookiecutter.__package_slug}}.celery import my_task

    # Verify task has Celery methods
    assert hasattr(my_task, "delay")
    assert hasattr(my_task, "apply_async")
    assert callable(my_task)
```

{%- endif %}

{%- if cookiecutter.include_quasiqueue == "y" %}

### Testing QuasiQueue

```python
@pytest.mark.asyncio
async def test_quasiqueue_job_execution():
    """Test QuasiQueue job execution."""
    from {{cookiecutter.__package_slug}}.qq import MyJobDefinition

    # Create job definition
    job_def = MyJobDefinition(input_data="test")

    # Execute job directly for testing
    result = await job_def.execute()
    assert result == expected_value

def test_quasiqueue_configuration():
    """Test QuasiQueue configuration."""
    from {{cookiecutter.__package_slug}}.qq import app, MyJobDefinition

    assert app is not None
    assert MyJobDefinition in app.job_classes
```

{%- endif %}

### Testing Settings

```python
def test_settings_load():
    """Test settings are loaded correctly."""
    from {{cookiecutter.__package_slug}}.settings import settings

    assert settings.project_name == "{{cookiecutter.__package_slug}}"
    assert settings.debug is not None

def test_settings_validation():
    """Test settings validation."""
    import os
    from unittest.mock import patch
    from {{cookiecutter.__package_slug}}.settings import Settings

    with patch.dict(os.environ, {"REQUIRED_VAR": "value"}):
        settings = Settings()
        assert settings.required_var == "value"

def test_settings_with_env_file():
    """Test loading settings from .env file."""
    from {{cookiecutter.__package_slug}}.settings import settings

    # Settings automatically loads from .env if present
    assert hasattr(settings, "project_name")
```

## Test Isolation and Independence

### Principles

1. **Each test is independent**: Tests should not depend on the order of execution
2. **Clean state**: Fixtures ensure each test starts with a clean state
3. **No side effects**: Tests should not affect other tests or external systems
4. **Idempotent**: Running tests multiple times produces the same results

### Database Test Isolation

{%- if cookiecutter.include_sqlalchemy == "y" %}

The `db_session_maker` fixture creates a fresh in-memory SQLite database for each test that needs it:

```python
@pytest_asyncio.fixture
async def db_session_maker(tmpdir):
    """Each test gets a fresh database."""
    test_database_url = f"sqlite+aiosqlite:///{tmpdir}/test_database.db"
    engine = create_async_engine(test_database_url, future=True, echo=False)

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield async_session_maker

    # Cleanup
    await engine.dispose()
```

This ensures:

- No test data leaks between tests
- Tests can be run in any order
- Tests can run in parallel safely
{%- endif %}

### Cache Test Isolation

{%- if cookiecutter.include_aiocache == "y" %}

When testing cache functionality, ensure caches are cleared between tests:

```python
@pytest.mark.asyncio
async def test_with_clean_cache():
    """Test with a clean cache."""
    from {{cookiecutter.__package_slug}}.services.cache import clear_cache

    # Clear all caches before test
    await clear_cache("memory")
    await clear_cache("persistent")

    # Your test here
    await set_cached("key", "value")
    result = await get_cached("key")
    assert result == "value"
```

{%- endif %}

## Coverage Requirements and Best Practices

### Coverage Goals

- **Minimum coverage**: 80% overall
- **Critical paths**: 100% coverage for critical business logic
- **New code**: All new features should include tests

### Checking Coverage

```bash
# Generate coverage report
make pytest

# View coverage for specific file
pytest --cov=./{{cookiecutter.__package_slug}}/services/cache.py tests/services/test_cache.py

# Fail if coverage is below threshold
pytest --cov=./{{cookiecutter.__package_slug}} --cov-fail-under=80 tests
```

### Coverage Configuration

Coverage is configured in `pyproject.toml`:

```toml
[tool.coverage.run]
concurrency = ["thread", "greenlet"]
omit = [
  "./{{cookiecutter.__package_slug}}/_version.py",
]
```

## Best Practices

1. **Write descriptive test names**: Test names should clearly describe what they test

   ```python
   # Good
   def test_user_creation_validates_email_format()

   # Bad
   def test_user()
   ```

2. **One assertion per test**: Keep tests focused on a single behavior

   ```python
   # Good
   def test_user_email_validation():
       assert validate_email("test@example.com") is True

   def test_user_email_validation_rejects_invalid():
       assert validate_email("invalid") is False

   # Bad (multiple unrelated assertions)
   def test_user_stuff():
       assert user.name == "Test"
       assert user.email_valid()
       assert user.age > 0
   ```

3. **Use fixtures for setup**: Avoid duplication by using fixtures

   ```python
   @pytest.fixture
   def sample_user():
       return User(name="Test", email="test@example.com")

   def test_user_name(sample_user):
       assert sample_user.name == "Test"
   ```

4. **Test both success and failure cases**: Test happy paths and error conditions

   ```python
   def test_divide_success():
       assert divide(10, 2) == 5

   def test_divide_by_zero_raises_error():
       with pytest.raises(ZeroDivisionError):
           divide(10, 0)
   ```

5. **Use parametrize for multiple test cases**: Test multiple inputs efficiently

   ```python
   @pytest.mark.parametrize("input,expected", [
       ("test@example.com", True),
       ("invalid", False),
       ("test@", False),
       ("@example.com", False),
   ])
   def test_email_validation(input, expected):
       assert validate_email(input) == expected
   ```

6. **Keep tests fast**: Use in-memory databases, mock external services, avoid sleep

   ```python
   # Good - uses in-memory database
   @pytest.mark.asyncio
   async def test_with_db(db_session):
       result = await query_database(db_session)
       assert result is not None

   # Bad - sleeps unnecessarily
   @pytest.mark.asyncio
   async def test_slow():
       await asyncio.sleep(5)  # Avoid this!
       assert True
   ```

7. **Test edge cases and boundary conditions**: Don't just test happy paths

   ```python
   @pytest.mark.parametrize("value", [0, -1, None, "", [], {}])
   def test_handles_edge_cases(value):
       result = process_value(value)
       assert result is not None
   ```

8. **Use async tests for async code**: Always use `@pytest.mark.asyncio` for async functions

   ```python
   # Good
   @pytest.mark.asyncio
   async def test_async_function():
       result = await async_operation()
       assert result == expected

   # Bad - won't work properly
   def test_async_function():
       result = async_operation()  # This returns a coroutine, not a result!
       assert result == expected
   ```

## Continuous Integration

Tests run automatically on every push and pull request via GitHub Actions. The CI pipeline:

1. **Runs all tests** with coverage reporting
2. **Checks code formatting** with ruff
3. **Performs type checking** with mypy
4. **Validates linting rules** with ruff
5. **Checks data formatting** with dapperdata
6. **Verifies TOML formatting** with toml-sort

See the [GitHub Actions documentation](./github.md) for more details on CI configuration.

## Troubleshooting Tests

### Common Issues

**Import Errors**

```bash
# Make sure the package is installed in development mode
make install
```

**Async Tests Not Running**

```python
# Make sure to mark async tests
@pytest.mark.asyncio
async def test_my_async_function():
    await async_operation()
```

**Database Fixture Issues**

```python
# Ensure you're using the correct fixture
@pytest.mark.asyncio
async def test_db_operation(db_session):  # Not db_session_maker
    result = await db_session.execute(query)
```

**Tests Pass Individually But Fail Together**

This usually indicates test isolation issues. Check:

- Are you cleaning up resources?
- Are tests sharing state through global variables?
- Are database transactions being rolled back?

**Coverage Not Including All Files**

Check `pyproject.toml` coverage configuration and ensure files aren't in the omit list.

## References

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy Testing Documentation](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)
