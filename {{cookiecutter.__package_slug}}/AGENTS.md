# Agent Instructions

You should always follow the best practices outlined in this document. If there is a valid reason why you cannot follow one of these practices, you should inform the user and document the reasons.

Before beginning any task, make sure you review the documentation (`docs/dev/` and `README.md`), the existing tests to understand the project, and the task runner (Makefile) to understand what dev tools are available and how to use them. You should review code related to your request to understand preferred style: for example, you should review other tests before writing a new test suite, or review existing routers before creating a new one.

## Best Practices

### General

* Assume the minimum version of Python is 3.10.
* Prefer async libraries and functions over synchronous ones.
* Always define dependencies and tool settings in `pyproject.toml`: never use `setup.py` or `setup.cfg` files.
* Prefer existing dependencies over adding new ones when possible.
* For complex code, always consider using third-party libraries instead of writing new code that has to be maintained.
* Use keyword arguments instead of positional arguments when calling functions and methods.
* Do not put `import` statements inside functions unless necessary to prevent circular imports. Imports should be at the top of the file.

### Security

* Always write secure code.
* Never hardcode sensitive data.
* Do not log sensitive data.
* All user input should be validated.

### Production Ready

* All generated code should be production ready.
* There should be no stubs "for production".
* There should not be any non-production logic branches in the main code package itself.
* Any code or package differences between Development and Production should be avoided unless absolutely necessary.

### Logging

* Do not use `print` for logging or debugging: use the `getLogger` logger instead.
* Each file should get its own logger using the `__name__` variable for a name.
* Use logging levels to allow developers to enable richer logging while testing than in production.
* Most caught exceptions should be logged with `logger.exception`.

### Commenting

* Comments should improve code readability and understandability.
* Comments should not simply exist for the sake of existing.
* Examples of good comments include unclear function names/parameters, decisions about settings or function choices, logic descriptions, variable definitions, security risks, edge cases, and advice for developers refactoring or expanding code.
* Comments should be concise, accurate, and add value to the codebase.

### Error Handling

* Do not suppress exceptions unless expected, and handle them properly when suppressing.
* When suppressing exceptions, log them using `logger.exception`.

### Typing

* Everything should be typed: function signatures (including return values), variables, and anything else.
* Use the union operator for multiple allowed types.
* Do not use `Optional`: use a union with `None` (i.e., `str | None`).
* Use typing library metaclasses instead of native types for objects and lists (i.e., `Dict[str, str]` and `List[str]` instead of `dict` or `list`).
* Avoid using `Any` unless absolutely necessary.
* If the schema is defined, use a `dataclass` with properly typed parameters instead of a `dict`.

### Settings

* Manage application settings with the `pydantic-settings` library.
* Sensitive configuration data should always use Pydantic `SecretStr` or `SecretBytes` types.
* Settings that are allowed to be unset should default to `None` instead of empty strings.
* Define settings with the Pydantic `Field` function and include descriptions for users.

{%- if cookiecutter.include_fastapi == "y" %}

### FastAPI

* APIs should adhere as closely as possible to REST principles, including appropriate use of GET/PUT/POST/DELETE HTTP verbs.
* All routes should use Pydantic models for input and output.
* Use different Pydantic models for inputs and outputs (i.e., creating a `Post` should require a `PostCreate` and return a `PostRead` model, not reuse the same model).
* Parameters in Pydantic models for user input should use the Field function with validation and descriptions.
{%- endif %}

{%- if cookiecutter.include_sqlalchemy == "y" %}

### SQLAlchemy

* Always use async SQLAlchemy APIs with SQLAlchemy 2.0 syntax.
* Represent database tables with the declarative class system.
* Use Alembic to define migrations.
* Migrations should be compatible with both SQLite and PostgreSQL.
* When creating queries, do not use implicit `and`: instead use the `and_` function (instead of `where(Model.parameter_a == A, Model.parameter_b == B)` do `where(and_(Model.parameter_a == A, Model.parameter_b == B))`).
{%- endif %}

{%- if cookiecutter.include_cli == "y" %}

### Typer

* Any CLI command or script that should be accessible to users should be exposed via the Typer library.
* The main CLI entrypoint should be `PACKAGE_NAME/cli.py`.
{%- endif %}

### Testing

* Do not wrap test functions in classes unless there is a specific technical reason: instead prefer single functions.
* All fixtures should be defined or imported in `conftest.py` so they are available to all tests.
* Do not use mocks to replace simple dataclasses or Pydantic models unless absolutely necessary: instead create an instance of the appropriate class with desired parameters.
* Use the FastAPI Test Client (preferably with a fixture) rather than calling FastAPI router classes directly.
* Use a test database fixture with memory-backed SQLite for tests requiring a database. Including a dependency override for this test database as part of the FastAPI App fixture is extremely useful.
* When adding new code, you should also add appropriate tests to cover that new code.
* The test suite file structure should mirror the main code file structure.

### Files

* Filenames should always be lowercase for better compatibility with case-insensitive filesystems.
* This includes documentation files, except standard files (like `README.md`, `LICENSE`, etc.).
* Developer documentation should live in `docs/dev`.
* New developer documents should be added to the table of contents in `docs/dev/README.md`.
* Files only meant for building containers should live in the `docker/` folder.
* Database models should live in `PACKAGE_NAME/models/`.
* The primary settings file should live in `PACKAGE_NAME/conf/settings.py`.

### Developer Environments

* Common developer tasks should be defined in the `makefile` to easy reuse.
* Developers should always be able to start a fully functional developer instance with `docker compose up`.
* Developer environments should be initialized with fake data for easy use.
* Developer settings should live in the `.env` file, which should be in `.gitignore`.
* A `.env.example` file should exist as a template for new developers to create their `.env` file and learn what variables to set.
* Python projects should always use virtual environments at `.venv` in the project root. This should be activated before running tests.
