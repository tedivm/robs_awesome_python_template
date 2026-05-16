---
name: sqlalchemy-models
description: "Create or modify SQLAlchemy models, queries, and Alembic migrations. Use when: defining new database tables, writing queries, creating migrations, checking model conventions, or understanding the database layer."
---

# SQLAlchemy Models and Migrations

> **context7**: If the `mcp_context7` tool is available, load the full `sqlalchemy` and `alembic` documentation before debugging, creating or modifying models or queries, or writing migrations:
> ```
> mcp_context7_resolve-library-id: "sqlalchemy"
> mcp_context7_get-library-docs: <resolved-id>
> mcp_context7_resolve-library-id: "alembic"
> mcp_context7_get-library-docs: <resolved-id>
> ```

Guidelines and patterns for database models, queries, and Alembic migrations in this codebase.

---

## Core Requirements

- Always use **async** SQLAlchemy APIs (never synchronous).
- Always use **SQLAlchemy 2.0** syntax.
- Represent database tables with the **declarative class system** (`Base` subclass).
- Use **Alembic** for all schema changes — never alter the schema manually.
- Migrations must be compatible with **both SQLite and PostgreSQL**.

---

## Model Definition

Models live in `{{cookiecutter.__package_slug}}/models/`. Import and extend the shared `Base` from `{{cookiecutter.__package_slug}}.models.base`.

```python
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from {{cookiecutter.__package_slug}}.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
```

### Typing Conventions

| Pattern                                  | Meaning                          |
| ---------------------------------------- | -------------------------------- |
| `Mapped[str]`                            | NOT NULL column                  |
| `Mapped[str \| None]`                    | NULLable column                  |
| `mapped_column(default=...)`             | Server-side / Python-side default |
| `mapped_column(primary_key=True)`        | Primary key                      |
| `mapped_column(unique=True)`             | Unique constraint                |
| `mapped_column(index=True)`              | Index                            |

---

## Querying

Always use `select()` with `await session.execute()`. For multiple criteria, always use `and_()` — never pass multiple comma-separated expressions to `.where()` (it breaks mypy type checking).

```python
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_active_user(session: AsyncSession, email: str, name: str) -> User | None:
    stmt = select(User).where(
        and_(
            User.email == email,
            User.name == name,
            User.is_active == True,
        )
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
```

### Common Query Patterns

```python
# Get one or None
result = await session.execute(select(User).where(User.id == user_id))
user = result.scalar_one_or_none()

# Get all matching
result = await session.execute(select(User).where(User.is_active == True))
users = result.scalars().all()

# Insert
session.add(new_user)
await session.flush()      # write to DB within transaction
await session.commit()     # or rely on context manager commit

# Delete
await session.delete(user)
await session.commit()
```

---

## Migrations

All schema changes must go through Alembic. Never modify the database schema directly.

> **CRITICAL**: Never modify an existing migration file that has already been committed. Existing migrations may have already run in production or on other developer machines. Editing them breaks the migration chain and corrupts databases that applied the original version. If a migration needs to be changed, create a new migration that makes the correction instead. **Ask the developer for explicit permission before modifying any existing migration file.**

### Create a Migration

```bash
make create_migration MESSAGE="description of changes"
```

**Always use `make create_migration` — never run `alembic revision` directly.** The make target spins up a fresh SQLite database, applies all existing migrations to verify the chain is intact, generates the new revision, then formats the output. Running `alembic revision` directly skips all of this.

Always review the generated migration before committing it — autogenerate is not perfect and may miss or misinterpret changes.

### Check for Missing Migrations

```bash
make check_ungenerated_migrations
```

Fails if there are model changes that haven't been captured in a migration file. Run this before committing.

### Update Schema Documentation

```bash
make document_schema
```

Regenerates the Paracelsus schema docs. Run after adding or modifying models.

### SQLite + PostgreSQL Compatibility

Migrations must work on both databases. Common pitfalls:

- **`server_default`**: Use `sa.text()` for SQL literals (e.g., `server_default=sa.text('false')`)
- **`Boolean` columns**: Name the type (e.g., `sa.Boolean(name="my_col_bool")`) so Alembic batch mode can properly regenerate its CHECK constraint during SQLite migrations
- **`Enum` types**: PostgreSQL creates a named enum type; SQLite does not. Use `native_enum=False` for cross-DB enums
- **`ALTER COLUMN`**: SQLite does not support `ALTER COLUMN`. Use `batch_alter_table` in Alembic for SQLite compatibility

```python
# In migration file — using batch for SQLite compatibility
def upgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column("email", existing_type=sa.String(), nullable=False)
```

---

## File Placement

- Models → `{{cookiecutter.__package_slug}}/models/<domain>.py`
- Base class → `{{cookiecutter.__package_slug}}/models/base.py` (do not modify)
- Migrations → `db/versions/<revision>_<description>.py` (auto-generated by Alembic)

---

## Style Checklist

Before submitting model or migration changes:

- [ ] Model extends `Base` from `{{cookiecutter.__package_slug}}.models.base`
- [ ] Model lives in `{{cookiecutter.__package_slug}}/models/`
- [ ] All columns explicitly typed with `Mapped[...]`
- [ ] All queries use `and_()` for multiple criteria
- [ ] Migration created with `make create_migration`
- [ ] `make check_ungenerated_migrations` passes
- [ ] `make document_schema` run after model changes
- [ ] Migration tested compatible with both SQLite and PostgreSQL

---

## Further Reading

- [docs/dev/database.md](../../docs/dev/database.md) — Full database developer guide covering session management, CRUD patterns, relationships, SQLite/PostgreSQL compatibility, and development vs. production configuration.
- [SQLAlchemy 2.0 Async Docs](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
