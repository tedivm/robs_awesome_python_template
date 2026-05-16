---
name: typer-cli
description: "Add or modify CLI commands using Typer. Use when: adding new CLI subcommands, wrapping async functions for CLI use, understanding the CLI entrypoint structure, or following the @syncify pattern for async commands."
---

# Typer CLI

> **context7**: If documentation tools are available, resolve and load the full `typer` documentation before making any changes to the CLI system:
> ```
> context7_resolve-library-id: "typer"
> context7_query-docs: <resolved-id> "your query here"
> ```

Any command or script that must be accessible to users must be exposed through the Typer library.

For full developer documentation see [docs/dev/cli.md](../../docs/dev/cli.md).

---

## CLI Structure

The CLI is registered in `pyproject.toml` as a project script pointing to `{{cookiecutter.__package_slug}}.cli:app`.

The main app is defined in `{{cookiecutter.__package_slug}}/cli.py`. Domain-specific subcommand groups live in separate `{{cookiecutter.__package_slug}}/cli_<domain>.py` files and are mounted onto the main app.

---

## Async Commands — `@syncify`

Typer runs commands synchronously, but this project uses async throughout (database access, HTTP calls, etc.). Use the `@syncify` decorator from `{{cookiecutter.__package_slug}}/cli.py` to bridge them:

```python
from {{cookiecutter.__package_slug}}.cli import syncify

@app.command()
@syncify
async def my_command(name: str) -> None:
    """This async function will run correctly from the CLI."""
    result = await some_async_operation(name)
    typer.echo(result)
```

**Critical**: `@app.command()` must appear **before** `@syncify` in decorator order. Do **not** use `asyncio.run()` directly — `syncify` handles the event loop correctly.

---

{%- if cookiecutter.include_sqlalchemy == "y" %}

### Database Access in CLI Commands

Use `get_session` from `{{cookiecutter.__package_slug}}.services.db` for database-backed commands. Always use it as an async context manager:

```python
from {{cookiecutter.__package_slug}}.services.db import get_session

@app.command()
@syncify
async def my_db_command() -> None:
    """Example command using database access."""
    async with get_session() as session:
        result = await session.execute(select(MyModel))
        items = result.scalars().all()
        for item in items:
            typer.echo(item.name)
```

---

{%- endif %}

## Parameter Pattern

Use `Annotated[]` for all arguments and options — it keeps the signature clean and is the Typer-recommended style:

```python
import typer
from typing import Annotated


app = typer.Typer()


@app.command()
def process(
    input_file: Annotated[str, typer.Argument(help="Path to the input file")],
    output_file: Annotated[str | None, typer.Option(help="Path to the output file")] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Enable verbose output")] = False,
) -> None:
    """Process the input file and generate output."""
    if verbose:
        typer.echo(f"Processing {input_file}...")
    typer.echo("Done!")
```

### Arguments vs Options

| Type                     | Typer class        | CLI usage                  |
| ------------------------ | ------------------ | -------------------------- |
| Positional (required)    | `typer.Argument()` | `cmd my-cmd value`         |
| Named flag/option        | `typer.Option()`   | `cmd my-cmd --flag x`      |
| Boolean flag pair        | `typer.Option(None, "--yes/--no")` | `cmd my-cmd --yes` |

---

## Adding a New Command Group

Create `{{cookiecutter.__package_slug}}/cli_<domain>.py`:

```python
# {{cookiecutter.__package_slug}}/cli_reports.py
import typer
from typing import Annotated

reports_app = typer.Typer(
    help="Report generation commands.",
    no_args_is_help=True,
)


@reports_app.command("generate")
def generate_report(
    output: Annotated[str, typer.Argument(help="Output file path")],
) -> None:
    """Generate a report and write it to the output path."""
    ...
```

Then mount it in `{{cookiecutter.__package_slug}}/cli.py`:

```python
from .cli_reports import reports_app

app.add_typer(reports_app, name="reports")
```

Use `no_args_is_help=True` on subapp `Typer()` instances so that `cmd reports` without arguments shows help rather than an error.

---

## Error Handling Pattern

For error output, write to stderr: `typer.echo(..., err=True)`. Exit with a non-zero code on failure: `raise typer.Exit(code=1)`. For clean exits: `raise typer.Exit()`.

---

## Style Checklist

- [ ] New commands in `{{cookiecutter.__package_slug}}/cli.py` or `{{cookiecutter.__package_slug}}/cli_<domain>.py`
- [ ] Async commands use `@syncify` (not `asyncio.run()`)
- [ ] `@app.command()` decorator appears **before** `@syncify`
- [ ] All parameters use `Annotated[type, typer.Argument/Option(...)]`
- [ ] Every command has a docstring (used as `--help` text)
- [ ] Subapp `Typer()` instances use `no_args_is_help=True`
- [ ] New subapp mounted in `{{cookiecutter.__package_slug}}/cli.py` with `app.add_typer(...)`
- [ ] Error output goes to `err=True`
- [ ] Failures raise `typer.Exit(code=1)` (not `sys.exit(1)` or bare exceptions)
