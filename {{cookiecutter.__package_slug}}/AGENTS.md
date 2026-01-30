# Agent Instructions

You must always follow the best practices outlined in this document. If there is a valid reason why you cannot follow one of these practices, you must inform the user and document the reasons.

Before beginning any task, make sure you review the documentation (`docs/dev/` and `README.md`), the existing tests to understand the project, and the task runner (Makefile) to understand what dev tools are available and how to use them. You must review code related to your request to understand preferred style: for example, you must review other tests before writing a new test suite, or review existing routers before creating a new one.

## Important Commands

### Development Environment Setup

```bash
make install # Install dependencies and set up virtual environment
make sync # Sync dependencies with uv.lock
make pre-commit # Install pre-commit hooks
```

### File Operations

```bash
git mv old_path new_path # ALWAYS use git mv for moving or renaming files, never use mv or file manipulation tools
```

**CRITICAL**: When moving or renaming files in a git repository, you MUST use `git mv` instead of regular `mv` or file manipulation tools. This ensures git properly tracks the file history and prevents issues with version control.

### Testing and Validation

```bash
make tests # Run all tests and checks (pytest, ruff, black, mypy, dapperdata, tomlsort)
make pytest # Run pytest with coverage report
make pytest_loud # Run pytest with debug logging enabled
uv run pytest # Run pytest directly with uv, adding any arguments and options needed
```

### Code Quality Checks

```bash
make ruff_check # Check code with ruff linter
make black_check # Check code formatting with ruff format using the black format
make mypy_check # Run type checking with mypy
make dapperdata_check # Check data file formatting
make tomlsort_check # Check TOML file linting and formatting
```

### Code Formatting (Auto-fix)

```bash
make chores # Run all formatting fixes (ruff, black, dapperdata, tomlsort)
make ruff_fixes # Auto-fix ruff issues
make black_fixes # Auto-format code with ruff using the black format
make dapperdata_fixes # Auto-format data files
make tomlsort_fixes # Auto-format TOML files
```

### Dependency Management

```bash
make lock # Update and lock dependencies
make lock-check # Check if lock file is up to date
uv add package_name # Add a new package dependency
uv add --group dev package_name # Add a dev dependency
uv remove package_name # Remove a package dependency
```

{%- if cookiecutter.include_sqlalchemy == "y" %}

### Database Operations

```bash
make create_migration MESSAGE="description of changes" # Create a new migration
make check_ungenerated_migrations # Check for ungenerated migrations
make document_schema # Update database schema documentation
```

{%- endif %}

{%- if cookiecutter.publish_to_pypi == "y" %}

### Packaging

```bash
make build # Build package distribution
```

{%- endif %}

{%- if cookiecutter.include_docker == "y" %}

### Docker

```bash
docker compose up -d # Start development environment and detach session
docker compose down # Stop development environment (preserves volumes)
docker compose down -v # Stop and remove development environment (including volumes)
docker compose restart # Restart all services without destroying containers or volumes
docker compose logs # View logs from all services
docker compose logs -f # Follow logs in real-time from all services
docker compose logs -f service_name # Follow logs for a specific service
docker compose ps # List running services and their status
docker compose exec service_name bash # Open a bash shell in a running service container
```

{%- endif %}

## Best Practices

### General

* Assume the minimum version of Python is 3.10.
* Prefer async libraries and functions over synchronous ones.
* Always define dependencies and tool settings in `pyproject.toml`: never use `setup.py` or `setup.cfg` files.
* Prefer existing dependencies over adding new ones when possible.
* For complex code, always consider using third-party libraries instead of writing new code that has to be maintained.
* Use keyword arguments instead of positional arguments when calling functions and methods.
* Do not put `import` statements inside functions unless necessary to prevent circular imports. Imports must be at the top of the file.

### Security

* Always write secure code.
* Never hardcode sensitive data.
* Do not log sensitive data.
* All user input must be validated.
* Never roll your own cryptography system.

### Production Ready

* All generated code must be production ready.
* There must be no stubs "for production".
* There must not be any non-production logic branches in the main code package itself.
* Any code or package differences between Development and Production must be avoided unless absolutely necessary.

### Logging

* Do not use `print` for logging or debugging: use the `getLogger` logger instead.
* Each file must get its own logger using the `__name__` variable for a name.
* Use logging levels to allow developers to enable richer logging while testing than in production.
* Most caught exceptions must be logged with `logger.exception`.

```python
from logging import getLogger
from typing import Dict

logger = getLogger(__name__)

def process_data(data: Dict[str, str]) -> None:
    logger.debug("Starting data processing")
    try:
        result = transform_data(data)
        logger.info("Data processed successfully")
    except ValueError as e:
        logger.exception("Failed to process data")
        raise
```

### Commenting

* Comments must improve code readability and understandability.
* Comments must not simply exist for the sake of existing.
* Examples of good comments include unclear function names/parameters, decisions about settings or function choices, logic descriptions, variable definitions, security risks, edge cases, and advice for developers refactoring or expanding code.
* Comments must be concise, accurate, and add value to the codebase.

### Error Handling

* Do not suppress exceptions unless expected, and handle them properly when suppressing.
* When suppressing exceptions, log them using `logger.exception`.

```python
# Bad: Suppressing without handling
try:
    risky_operation()
except Exception:
    pass  # Never do this

# Good: Proper handling with logging
try:
    risky_operation()
except ValueError as e:
    logger.exception("Operation failed with invalid value")
    raise
except FileNotFoundError:
    logger.warning("File not found, using defaults")
    use_defaults()
```

### Typing

* Everything must be typed: function signatures (including return values), variables, and anything else.
* Use the union operator for multiple allowed types.
* Do not use `Optional`: use a union with `None` (i.e., `str | None`).
* Use typing library metaclasses instead of native types for objects and lists (i.e., `Dict[str, str]` and `List[str]` instead of `dict` or `list`).
* Avoid using `Any` unless absolutely necessary.
* If the schema is defined, use a `dataclass` with properly typed parameters instead of a `dict`.

```python
from dataclasses import dataclass
from typing import Dict, List

# Good: Proper typing
@dataclass
class User:
    name: str
    email: str
    age: int | None = None

def process_users(users: List[User], tags: Dict[str, str]) -> List[str]:
    results: List[str] = []
    for user in users:
        results.append(user.name)
    return results

# Bad: Using dict instead of dataclass (and using native types)
def process_users_bad(users: list[dict], config: dict) -> list:
    pass  # Avoid this
```

### Settings

* Manage application settings with the `pydantic-settings` library.
* The main Settings class is located in `PACKAGE_NAME/conf/settings.py` - update this existing class rather than creating new ones.
* Sensitive configuration data must always use Pydantic `SecretStr` or `SecretBytes` types.
* Settings that are allowed to be unset must default to `None` instead of empty strings.
* Define settings with the Pydantic `Field` function and include descriptions for users.

```python
# File: {{cookiecutter.__package_slug}}/conf/settings.py
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    project_name: str = Field(default="MyProject", description="Project name")

    # Good: Using SecretStr for sensitive data
    database_password: SecretStr = Field(
        description="Database password"
    )

    # Good: Optional field defaults to None
    api_key: str | None = Field(
        default=None,
        description="Optional API key for external service"
    )

    # Good: Using Field with description
    max_connections: int = Field(
        default=10,
        description="Maximum number of database connections"
    )
```

{%- if cookiecutter.include_fastapi == "y" %}

### FastAPI

* APIs must adhere as closely as possible to REST principles, including appropriate use of GET/PUT/POST/DELETE HTTP verbs.
* All routes must use Pydantic models for input and output.
* Use different Pydantic models for inputs and outputs (i.e., creating a `Post` must require a `PostCreate` and return a `PostRead` model, not reuse the same model).
* Parameters in Pydantic models for user input must use the Field function with validation and descriptions.

```python
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter()

class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200, description="Post title")
    content: str = Field(min_length=1, description="Post content")

class PostRead(BaseModel):
    id: UUID
    title: str
    content: str
    created_at: str

class PostUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    content: str | None = None

@router.post("/posts", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate) -> PostRead:
    # Use different model for input (PostCreate) and output (PostRead)
    pass

@router.get("/posts/{post_id}", response_model=PostRead)
async def get_post(post_id: UUID) -> PostRead:
    pass

@router.put("/posts/{post_id}", response_model=PostRead)
async def update_post(post_id: UUID, post: PostUpdate) -> PostRead:
    pass

@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: UUID) -> None:
    pass
```

{%- endif %}

{%- if cookiecutter.include_sqlalchemy == "y" %}

### SQLAlchemy

* Always use async SQLAlchemy APIs with SQLAlchemy 2.0 syntax.
* Represent database tables with the declarative class system.
* Use Alembic to define migrations.
* Migrations must be compatible with both SQLite and PostgreSQL.
* When creating queries, do not use implicit `and`: instead use the `and_` function (instead of `where(Model.parameter_a == A, Model.parameter_b == B)` do `where(and_(Model.parameter_a == A, Model.parameter_b == B))`).

```python
from uuid import UUID, uuid4

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from {{cookiecutter.__package_slug}}.models.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

# Good: Async query with explicit and_()
async def get_active_user(session: AsyncSession, email: str, name: str) -> User | None:
    stmt = select(User).where(
        and_(
            User.email == email,
            User.name == name,
            User.is_active == True
        )
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

# Bad: Implicit and (avoid this)
async def get_user_bad(session: AsyncSession, email: str, name: str) -> User | None:
    stmt = select(User).where(User.email == email, User.name == name)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
```

{%- endif %}

{%- if cookiecutter.include_cli == "y" %}

### Typer

* Any CLI command or script that must be accessible to users must be exposed via the Typer library.
* The main CLI entrypoint must be `PACKAGE_NAME/cli.py`.
* For async commands, use the `@syncify` decorator provided in `cli.py` to convert async functions to sync for Typer compatibility.

```python
import typer
from typing import Annotated

from {{cookiecutter.__package_slug}}.cli import syncify

app = typer.Typer()

@app.command()
def process(
    input_file: Annotated[str, typer.Argument(help="Path to input file")],
    output_file: Annotated[str | None, typer.Option(help="Path to output file")] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Enable verbose output")] = False,
) -> None:
    """Process the input file and generate output."""
    if verbose:
        typer.echo(f"Processing {input_file}...")
    # Processing logic here
    typer.echo("Done!")

@app.command()
@syncify
async def fetch(
    url: Annotated[str, typer.Argument(help="URL to fetch data from")],
) -> None:
    """Fetch data from a URL asynchronously."""
    # Async operations here (database queries, HTTP requests, etc.)
    typer.echo(f"Fetching from {url}")

if __name__ == "__main__":
    app()
```

{%- endif %}

### Testing

* Do not wrap test functions in classes unless there is a specific technical reason: instead prefer single functions.
* All fixtures must be defined or imported in `conftest.py` so they are available to all tests.
* Do not use mocks to replace simple dataclasses or Pydantic models unless absolutely necessary: instead create an instance of the appropriate class with desired parameters.
* Use the FastAPI Test Client (preferably with a fixture) rather than calling FastAPI router classes directly.
* Use a test database fixture with memory-backed SQLite for tests requiring a database. Including a dependency override for this test database as part of the FastAPI App fixture is extremely useful.
* When adding new code, you must also add appropriate tests to cover that new code.
* The test suite file structure must mirror the main code file structure.

### Files

* Filenames must always be lowercase for better compatibility with case-insensitive filesystems.
* This includes documentation files, except standard files (like `README.md`, `LICENSE`, etc.).
* Developer documentation must live in `docs/dev`.
* New developer documents must be added to the table of contents in `docs/dev/README.md`.
* Files only meant for building containers must live in the `docker/` folder.
* Database models must live in `PACKAGE_NAME/models/`.
* The primary settings file must live in `PACKAGE_NAME/conf/settings.py`.

### Developer Environments

* Common developer tasks must be defined in the `makefile` to easy reuse.
* Developers must always be able to start a fully functional developer instance with `docker compose up`.
* Developer environments must be initialized with fake data for easy use.
* Developer settings must live in the `.env` file, which must be in `.gitignore`.
* A `.env.example` file must exist as a template for new developers to create their `.env` file and learn what variables to set.
* Python projects must always use virtual environments at `.venv` in the project root. This must be activated before running tests.
* Use `uv` for Python version management and package installation instead of pyenv and pip for significantly faster installations and automatic Python version handling.
