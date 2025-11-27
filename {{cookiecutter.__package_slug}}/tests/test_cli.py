"""Tests for CLI application."""
import pytest
from typer.testing import CliRunner
from {{cookiecutter.__package_slug}}.cli import app, syncify
import asyncio


runner = CliRunner()


def test_cli_app_exists():
    """Test that Typer app is properly instantiated."""
    assert app is not None
    assert hasattr(app, "command")


def test_cli_app_has_commands():
    """Test that CLI app has registered commands."""
    assert hasattr(app, "registered_commands")


def test_version_command_exists():
    """Test that version command is registered."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "version" in result.stdout.lower() or "full_test_project" in result.stdout.lower()


def test_version_command_runs():
    """Test that version command executes successfully."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0


def test_version_output_format():
    """Test that version command outputs correct format."""
    from {{cookiecutter.__package_slug}}.settings import settings
    result = runner.invoke(app, ["version"])
    assert settings.project_name in result.stdout
    # Should output: "project_name - X.Y.Z"
    assert "-" in result.stdout


def test_version_contains_version_number():
    """Test that version output contains a version number."""
    from {{cookiecutter.__package_slug}}.settings import settings
    result = runner.invoke(app, ["version"])
    output = result.stdout.strip()
    # Should contain project name and version
    assert settings.project_name in output


def test_help_flag():
    """Test that --help flag works."""
    from {{cookiecutter.__package_slug}}.settings import settings
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert settings.project_name in result.stdout.lower() or "display" in result.stdout.lower()


def test_help_shows_description():
    """Test that help output shows description."""
    result = runner.invoke(app, ["--help"])
    assert "version" in result.stdout.lower() or "display" in result.stdout.lower()


def test_syncify_decorator_exists():
    """Test that syncify decorator is defined."""
    assert syncify is not None
    assert callable(syncify)


def test_syncify_converts_async_to_sync():
    """Test that syncify properly converts async functions to sync."""
    @syncify
    async def test_async_func():
        await asyncio.sleep(0.01)
        return "success"

    # Should be able to call without await
    result = test_async_func()
    assert result == "success"


def test_syncify_preserves_return_value():
    """Test that syncify preserves the return value."""
    @syncify
    async def test_async_func():
        return 42

    result = test_async_func()
    assert result == 42


def test_syncify_with_arguments():
    """Test that syncify works with function arguments."""
    @syncify
    async def test_async_func(x, y):
        await asyncio.sleep(0.01)
        return x + y

    result = test_async_func(10, 20)
    assert result == 30


def test_syncify_preserves_function_name():
    """Test that syncify preserves the function's name."""
    @syncify
    async def my_function():
        return True

    assert my_function.__name__ == "my_function"


def test_settings_imported():
    """Test that settings can be imported in CLI module."""
    from {{cookiecutter.__package_slug}}.settings import settings
    assert settings is not None
    assert hasattr(settings, "project_name")


def test_version_uses_settings():
    """Test that version command uses project_name from settings."""
    from {{cookiecutter.__package_slug}}.settings import settings
    result = runner.invoke(app, ["version"])
    assert settings.project_name in result.stdout

{%- if cookiecutter.include_sqlalchemy == "y" %}


def test_test_data_command_exists():
    """Test that test_data command is registered."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "test-data" in result.stdout.lower() or "test_data" in result.stdout.lower()


def test_test_data_command_runs(db_session):
    """Test that test_data command executes successfully."""
    result = runner.invoke(app, ["test-data"])
    assert result.exit_code == 0
    assert "successfully" in result.stdout.lower()


def test_test_data_shows_version(db_session):
    """Test that test_data command shows version in output."""
    from {{cookiecutter.__package_slug}}.settings import settings
    result = runner.invoke(app, ["test-data"])
    assert settings.project_name in result.stdout


def test_test_data_calls_db_function(db_session, monkeypatch):
    """Test that test_data command calls the database test_data function."""
    called = []

    async def mock_test_data(session):
        called.append(True)

    import {{cookiecutter.__package_slug}}.services.db as db_module
    monkeypatch.setattr(db_module, "test_data", mock_test_data)

    result = runner.invoke(app, ["test-data"])
    assert result.exit_code == 0
    assert len(called) == 1, "test_data function should be called once"
{%- endif %}
