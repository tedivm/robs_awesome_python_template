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

**CRITICAL**: When moving or renaming files in a git repository, you MUST use `git mv` instead of regular `mv` or file manipulation tools. This ensures git properly tracks file history and prevents issues with version control. The only exception to this is if you are moving files which are not tracked in git, as in that case `git mv` will have no effect.

### Testing and Validation

```bash
make tests # Run all tests and checks (pytest, ruff, black, mypy, prettier, tomlsort)
make pytest # Run pytest with coverage report
make pytest_loud # Run pytest with debug logging enabled
uv run pytest # Run pytest directly with uv, adding any arguments and options needed
```

For full testing conventions, fixture patterns, and database test strategies, see the `python-testing` skill.

### Code Quality Checks

```bash
make ruff_check # Check code with ruff linter
make black_check # Check code formatting with ruff format using the black format
make mypy_check # Run type checking with mypy
make prettier_check # Check markdown/json/yaml/etc formatting with prettier
make tomlsort_check # Check TOML file linting and formatting
```

### Code Formatting (Auto-fix)

```bash
make chores # Run all formatting fixes (ruff, black, prettier, tomlsort)
make ruff_fixes # Auto-fix ruff issues
make black_fixes # Auto-format code with ruff using the black format
make prettier_fixes # Auto-format markdown/json/yaml/etc
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

For full model conventions, query patterns, and migration workflows, see the `sqlalchemy-models` skill.

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
```

For the full Docker Compose command reference and common workflows, see the `docker-compose` skill.

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

Manage application settings with `pydantic-settings` in `{{cookiecutter.__package_slug}}/conf/settings.py` — update the existing class, never create a new one. Use `SecretStr` / `SecretBytes` for sensitive data. Optional settings default to `None`, never `""`. All fields use `Field(description=...)`.

See the `pydantic-settings` skill for full conventions and examples.

{%- if cookiecutter.include_fastapi == "y" %}

### FastAPI

Follow REST principles with appropriate HTTP verbs (GET/POST/PUT/DELETE). Use separate Pydantic models for input and output (`PostCreate` / `PostRead` / `PostUpdate`). Never reuse the same model. All input model fields use `Field()` with validation and a description.

See the `fastapi-routes` skill for full conventions, the router pattern, and code examples.

{%- endif %}

{%- if cookiecutter.include_sqlalchemy == "y" %}

### SQLAlchemy

Use async SQLAlchemy 2.0 with the declarative class system. Models live in `{{cookiecutter.__package_slug}}/models/`. Use Alembic for all schema changes (migrations must work on both SQLite and PostgreSQL). Always use explicit `and_()` in queries — no implicit AND.

See the `sqlalchemy-models` skill for full conventions, model patterns, migration commands, and SQLite/PostgreSQL compatibility notes.

{%- endif %}

{%- if cookiecutter.include_cli == "y" %}

### Typer

Expose user-facing commands via Typer. The main CLI entrypoint is `{{cookiecutter.__package_slug}}/cli.py`. Use the `@syncify` decorator (from `{{cookiecutter.__package_slug}}/cli.py`) for async commands — never use `asyncio.run()` directly. Use `Annotated[]` for all arguments and options.

See the `typer-cli` skill for full patterns and examples.

{%- endif %}

### Testing

Prefer standalone test functions over test classes. All fixtures must be in `conftest.py`. Test file structure mirrors the main code structure. Do not mock simple dataclasses or Pydantic models — construct real instances. When adding new code, add tests to cover it.

See the `python-testing` skill for FastAPI test client patterns, memory SQLite database fixtures, and testing conventions.

### Files

* Filenames must always be lowercase for better compatibility with case-insensitive filesystems.
* This includes documentation files, except standard files (like `README.md`, `LICENSE`, etc.).
* Developer documentation must live in `docs/dev`.
* New developer documents must be added to the table of contents in `docs/dev/README.md`.
* Files only meant for building containers must live in the `docker/` folder.
* Database models must live in `{{cookiecutter.__package_slug}}/models/`.
* The primary settings file must live in `{{cookiecutter.__package_slug}}/conf/settings.py`.

### Developer Environments

* Common developer tasks must be defined in the `makefile` to ease reuse.
* Developers must always be able to start a fully functional developer instance with `docker compose up`.
* Developer environments must be initialized with fake data for easy use.
* Developer settings must live in the `.env` file, which must be in `.gitignore`.
* A `.env.example` file must exist as a template for new developers to create their `.env` file and learn what variables to set.
* Python projects must always use virtual environments at `.venv` in the project root. This must be activated before running tests.
* Use `uv` for Python version management and package installation instead of pyenv and pip for significantly faster installations and automatic Python version handling.
