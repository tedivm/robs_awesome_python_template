# CLI

This project uses [Typer](https://typer.tiangolo.com/) for building command-line interfaces, with [Click](https://click.palletsprojects.com/) as the underlying framework.

## Configuration

The CLI application is defined in `{{cookiecutter.__package_slug}}/cli.py` and automatically configured as an entry point in `pyproject.toml`:

```toml
[project.scripts]
{{cookiecutter.__package_slug}} = "{{cookiecutter.__package_slug}}.cli:app"
```

After installation, the CLI is available as the `{{cookiecutter.__package_slug}}` command.

## Basic Usage

### Getting Help

View all available commands:

```bash
{{cookiecutter.__package_slug}} --help
```

Get help for a specific command:

```bash
{{cookiecutter.__package_slug}} command-name --help
```

### Running Commands

Execute a command:

```bash
{{cookiecutter.__package_slug}} my-command --option value argument
```

## Adding Commands

### Simple Command

Add a basic command to `{{cookiecutter.__package_slug}}/cli.py`:

```python
import typer

app = typer.Typer()

@app.command()
def hello(name: str):
    """Greet someone by name."""
    typer.echo(f"Hello, {name}!")
```

Usage:

```bash
{{cookiecutter.__package_slug}} hello "World"
# Output: Hello, World!
```

### Command with Options

Add commands with optional flags:

```python
@app.command()
def process(
    input_file: str,
    output_file: str = typer.Option(None, "--output", "-o", help="Output file path"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
):
    """Process an input file and optionally save to output."""
    if verbose:
        typer.echo(f"Processing {input_file}...")

    # Processing logic here

    if output_file:
        typer.echo(f"Saved to {output_file}")
```

Usage:

```bash
{{cookiecutter.__package_slug}} process input.txt --output output.txt --verbose
{{cookiecutter.__package_slug}} process input.txt -o output.txt -v
```

### Command with Type Validation

Typer automatically validates types:

```python
from pathlib import Path
from enum import Enum

class OutputFormat(str, Enum):
    json = "json"
    yaml = "yaml"
    csv = "csv"

@app.command()
def export(
    count: int = typer.Option(10, min=1, max=1000, help="Number of records"),
    format: OutputFormat = typer.Option(OutputFormat.json, help="Output format"),
    output: Path = typer.Option(Path("output.txt"), help="Output file"),
):
    """Export data in specified format."""
    typer.echo(f"Exporting {count} records as {format.value} to {output}")
```

Usage:

```bash
{{cookiecutter.__package_slug}} export --count 50 --format yaml --output data.yaml
```

### Interactive Prompts

Use prompts for interactive input:

```python
@app.command()
def configure():
    """Interactive configuration setup."""
    name = typer.prompt("What is your name?")
    age = typer.prompt("What is your age?", type=int)
    password = typer.prompt("Enter password", hide_input=True)

    if typer.confirm("Save configuration?"):
        typer.echo("Configuration saved!")
    else:
        typer.echo("Configuration discarded")
```

## Async Commands

### Using the Syncify Decorator

The template includes a `syncify` decorator for async CLI commands:

```python
from {{cookiecutter.__package_slug}}.cli import syncify
import httpx

@app.command()
@syncify
async def fetch_data(url: str):
    """Fetch data from a URL asynchronously."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        typer.echo(f"Status: {response.status_code}")
        return response.text
```

### Database Access

Use async database operations in CLI commands:

```python
from {{cookiecutter.__package_slug}}.services.db import get_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

@app.command()
@syncify
async def list_users():
    """List all users from the database."""
    engine = await get_engine()
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession)

    async with SessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()

        for user in users:
            typer.echo(f"User: {user.username} ({user.email})")
```

## Organizing Commands

### Command Groups

Organize related commands into groups:

```python
import typer

app = typer.Typer()
{%- if cookiecutter.include_sqlalchemy == "y" %}

# Create subcommands
db_app = typer.Typer()
user_app = typer.Typer()

# Add subcommands to main app
app.add_typer(db_app, name="db", help="Database management commands")
app.add_typer(user_app, name="user", help="User management commands")

# Define commands in each group
@db_app.command("migrate")
def db_migrate():
    """Run database migrations."""
    typer.echo("Running migrations...")

@db_app.command("seed")
def db_seed():
    """Seed database with initial data."""
    typer.echo("Seeding database...")

@user_app.command("create")
def user_create(username: str, email: str):
    """Create a new user."""
    typer.echo(f"Creating user {username} ({email})")

@user_app.command("list")
def user_list():
    """List all users."""
    typer.echo("Listing users...")
```

{%- endif %}

Usage:

```bash
{{cookiecutter.__package_slug}} db migrate
{{cookiecutter.__package_slug}} db seed
{{cookiecutter.__package_slug}} user create john john@example.com
{{cookiecutter.__package_slug}} user list
```

### Separate Command Modules

For larger projects, split commands into separate files:

```
{{cookiecutter.__package_slug}}/
├── cli.py              # Main app
└── commands/
    ├── __init__.py
    ├── database.py     # Database commands
    └── users.py        # User commands
```

In `cli.py`:

```python
from {{cookiecutter.__package_slug}}.commands import database, users

app = typer.Typer()
app.add_typer(database.app, name="db")
app.add_typer(users.app, name="user")
```

## Output Formatting

### Styled Output

Use typer's styling for colored output:

```python
@app.command()
def status():
    """Check system status."""
    typer.secho("✓ System operational", fg=typer.colors.GREEN, bold=True)
    typer.secho("⚠ Warning: High memory usage", fg=typer.colors.YELLOW)
    typer.secho("✗ Error: Database connection failed", fg=typer.colors.RED)
```

### Progress Bars

Show progress for long-running operations:

```python
import time

@app.command()
def process_items():
    """Process multiple items with progress bar."""
    items = range(100)

    with typer.progressbar(items, label="Processing") as progress:
        for item in progress:
            # Simulate processing
            time.sleep(0.1)

    typer.echo("Processing complete!")
```

### Tables

For structured output, use rich tables:

```python
from rich.console import Console
from rich.table import Table

@app.command()
def report():
    """Generate a formatted report."""
    console = Console()

    table = Table(title="User Report")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Email", style="green")

    table.add_row("1", "John Doe", "john@example.com")
    table.add_row("2", "Jane Smith", "jane@example.com")

    console.print(table)
```

## Error Handling

### Graceful Error Messages

Handle errors with user-friendly messages:

```python
@app.command()
def delete_user(user_id: int):
    """Delete a user by ID."""
    try:
        # Delete logic here
        if not user_exists(user_id):
            typer.secho(f"Error: User {user_id} not found", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        typer.echo(f"User {user_id} deleted successfully")
    except Exception as e:
        typer.secho(f"Error: {str(e)}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
```

### Exit Codes

Use proper exit codes for scripts:

```python
@app.command()
def validate_config():
    """Validate configuration file."""
    if config_is_valid():
        typer.echo("Configuration is valid")
        raise typer.Exit(code=0)  # Success
    else:
        typer.secho("Configuration has errors", fg=typer.colors.RED)
        raise typer.Exit(code=1)  # Failure
```

## Testing CLI Commands

### Using CliRunner

The project uses Typer's `CliRunner` for testing CLI commands. Create a module-level runner instance for reuse across tests:

```python
# tests/test_cli.py
from typer.testing import CliRunner
from {{cookiecutter.__package_slug}}.cli import app, syncify
import asyncio

# Module-level runner instance
runner = CliRunner()


def test_cli_app_exists():
    """Test that Typer app is properly instantiated."""
    assert app is not None
    assert hasattr(app, "command")


def test_version_command_runs():
    """Test that version command executes successfully."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "{{cookiecutter.__package_slug}}" in result.stdout.lower()


def test_help_command():
    """Test that help command works."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    # Check for command names in help output
```

### Testing Commands with Arguments

```python
def test_command_with_args():
    """Test command that takes arguments."""
    result = runner.invoke(app, ["process", "input.txt"])
    assert result.exit_code == 0
    assert "Processing input.txt" in result.output


def test_command_with_options():
    """Test command with optional flags."""
    result = runner.invoke(app, ["process", "input.txt", "--verbose"])
    assert result.exit_code == 0
    assert "Processing input.txt" in result.output
```

### Testing Async Commands

Test async commands that use the `syncify` decorator:

```python
def test_syncify_decorator():
    """Test the syncify decorator for async CLI commands."""
    @syncify
    async def async_function():
        await asyncio.sleep(0.01)
        return "success"

    result = async_function()
    assert result == "success"


@app.command()
@syncify
async def async_example():
    """Example async command."""
    await asyncio.sleep(0.01)
    print("Async command completed")


def test_async_command():
    """Test async CLI command."""
    result = runner.invoke(app, ["async-example"])
    assert result.exit_code == 0
    assert "Async command completed" in result.stdout
```

### Testing with Environment Variables

Use pytest's `monkeypatch` to set environment variables for tests:

```python
def test_with_env_vars(monkeypatch):
    """Test command that uses environment variables."""
    monkeypatch.setenv("API_KEY", "test-key-12345")
    monkeypatch.setenv("DEBUG", "True")

    result = runner.invoke(app, ["fetch-data"])
    assert result.exit_code == 0


def test_settings_in_cli(monkeypatch):
    """Test that CLI commands can access settings."""
    monkeypatch.setenv("PROJECT_NAME", "Test Project")

    result = runner.invoke(app, ["show-config"])
    assert result.exit_code == 0
    assert "Test Project" in result.stdout
```

### Testing Error Handling

```python
def test_command_with_invalid_input():
    """Test command error handling."""
    result = runner.invoke(app, ["process", "nonexistent.txt"])
    assert result.exit_code != 0
    assert "Error" in result.stdout or "not found" in result.stdout.lower()


def test_command_validation():
    """Test that command validates input."""
    # Test with invalid argument type
    result = runner.invoke(app, ["process-count", "not-a-number"])
    assert result.exit_code != 0
```

## Best Practices

1. **Clear Command Names**: Use descriptive, action-oriented names (e.g., `create-user`, `export-data`)

2. **Comprehensive Help Text**: Always add docstrings to commands - they become the help text:

   ```python
   @app.command()
   def my_command(arg: str):
       """
       This is the command description shown in --help.

       Provide details about what the command does and any important notes.
       """
       pass
   ```

3. **Validate Input Early**: Use Typer's type system and validation to catch errors before processing:

   ```python
   @app.command()
   def process(
       count: int = typer.Option(..., min=1, max=1000),
       file: Path = typer.Option(..., exists=True, file_okay=True),
   ):
       pass
   ```

4. **Use Enums for Choices**: Define fixed sets of options with enums instead of strings

5. **Provide Defaults**: Always provide sensible defaults for optional parameters

6. **Exit with Appropriate Codes**: Use exit code 0 for success, non-zero for errors

7. **Use Progress Indicators**: For long-running operations, show progress to keep users informed

## Running the CLI

### During Development

```bash
# Install in editable mode
pip install -e .

# Run commands
{{cookiecutter.__package_slug}} --help
{{cookiecutter.__package_slug}} my-command
```

### After Installation

```bash
# Regular installation
pip install .

# Commands are available globally
{{cookiecutter.__package_slug}} --help
```

### Direct Python Execution

```bash
# Without installation
python -m {{cookiecutter.__package_slug}}.cli --help
```

## References

- [Typer Documentation](https://typer.tiangolo.com/)
- [Click Documentation](https://click.palletsprojects.com/)
- [Rich Documentation](https://rich.readthedocs.io/) (for advanced formatting)
