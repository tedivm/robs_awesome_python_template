---
name: makefile
description: "Complete reference for all make targets in the project. Use when: looking up the right make command for any task — setup, testing, linting, formatting, database, packaging, or cleanup."
---

# Makefile Reference

All developer tasks are exposed as `make` targets. Run from the project root.

---

## Setup

| Target        | What it does                                                    |
| ------------- | --------------------------------------------------------------- |
| `make install` | Install Python deps, create `.venv` (first-time setup)         |
| `make sync`   | Sync Python deps with `uv.lock` (after pulling changes)         |
| `make pre-commit` | Install pre-commit hooks                                   |
| `make lock`   | Upgrade and relock all dependencies                             |
| `make lock-check` | Verify lock file is up to date without changing it         |

---

## Testing

| Target          | What it does                                                      |
| --------------- | ----------------------------------------------------------------- |
{%- if cookiecutter.include_sqlalchemy == "y" %}
| `make tests`    | Run **everything**: pytest, ruff, black, mypy, prettier, TOML, paracelsus       |
{%- else %}
| `make tests`    | Run **everything**: pytest, ruff, black, mypy, prettier, TOML formatting       |
{%- endif %}
| `make pytest`   | Run pytest with coverage report                                  |
| `make pytest_loud` | Run pytest with `DEBUG` log output enabled                    |

---

## Code Quality Checks

These check only — they do not auto-fix.

| Target                          | What it checks                                    |
| ------------------------------- | ------------------------------------------------- |
| `make ruff_check`               | Ruff linter                                       |
| `make black_check`              | Ruff formatter (black style)                      |
| `make mypy_check`               | Type checking (mypy)                              |
| `make prettier_check`           | Markdown, JSON, YAML, TOML formatting (prettier)  |
| `make tomlsort_check`           | TOML file formatting (tombi)                      |

{%- if cookiecutter.include_sqlalchemy == "y" %}

| `make paracelsus_check`         | Database schema docs are up to date               |
| `make check_ungenerated_migrations` | No pending Alembic migration changes          |

{%- endif %}

---

## Code Formatting (Auto-fix)

| Target                   | What it fixes                                          |
| ------------------------ | ------------------------------------------------------ |
{%- if cookiecutter.include_sqlalchemy == "y" %}
| `make chores`            | Run **all** auto-fixes: ruff, format, prettier, TOML, schema docs   |
{%- else %}
| `make chores`            | Run **all** auto-fixes: ruff, format, prettier, TOML   |
{%- endif %}
| `make ruff_fixes`        | Auto-fix ruff lint issues                              |
| `make black_fixes`       | Auto-format Python code (black style via ruff)         |
| `make prettier_fixes`    | Auto-format markdown/JSON/YAML/TOML                    |
| `make tomlsort_fixes`    | Auto-format TOML files (tombi)                         |

**Typical workflow before committing:** `make chores && make tests`

---

{%- if cookiecutter.include_sqlalchemy == "y" %}

## Database

| Target                                          | What it does                                            |
| ----------------------------------------------- | ------------------------------------------------------- |
| `make create_migration MESSAGE="description"`   | Generate a new Alembic migration from model changes     |
| `make check_ungenerated_migrations`             | Fail if there are model changes without a migration     |
| `make run_migrations`                           | Apply all pending migrations (`alembic upgrade head`)   |
| `make document_schema`                          | Regenerate `docs/dev/database.md` from current models   |
| `make paracelsus_check`                         | Verify schema docs are current (read-only check)        |
| `make reset_db`                                 | Wipe local SQLite test DB and reapply all migrations    |

`create_migration` requires a `MESSAGE` argument:

```bash
make create_migration MESSAGE="add email_verified column to users"
```

---

{%- endif %}

{%- if cookiecutter.publish_to_pypi == "y" %}

## Packaging

| Target             | What it does                                  |
| ------------------ | --------------------------------------------- |
| `make build`       | Build Python package distribution (sdist + wheel) |

---

{%- endif %}

## Quick Reference by Task

| I want to…                                | Run                                  |
| ----------------------------------------- | ------------------------------------ |
| Set up for the first time                 | `make install`                       |
| Run all tests before a PR                 | `make tests`                         |
| Fix all formatting issues                 | `make chores`                        |
| Check types only                          | `make mypy_check`                    |
{%- if cookiecutter.include_sqlalchemy == "y" %}
| Add a database migration                  | `make create_migration MESSAGE="..."` |
| Regenerate DB docs after model changes    | `make document_schema`               |
{%- endif %}
| Run only Python tests with verbose output | `make pytest_loud`                   |
| Update dependencies                       | `make lock && make sync`             |

---

## Further Reading

- [docs/dev/makefile.md](../../docs/dev/makefile.md) — Full makefile developer guide with detailed explanations of every target, shell autocomplete setup, and usage examples.
