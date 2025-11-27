"""Tests for QuasiQueue configuration and functionality."""
import pytest
from {{cookiecutter.__package_slug}}.qq import runner, writer, reader


def test_runner_exists():
    """Test that QuasiQueue runner is properly instantiated."""
    assert runner is not None


def test_runner_has_name():
    """Test that runner has a project name."""
    assert hasattr(runner, "name") or hasattr(runner, "project_name")


def test_runner_has_settings():
    """Test that runner has settings configured."""
    assert hasattr(runner, "settings")
    assert runner.settings is not None


def test_runner_has_reader():
    """Test that runner has a reader function."""
    assert hasattr(runner, "reader")
    assert runner.reader is not None


def test_runner_has_writer():
    """Test that runner has a writer function."""
    assert hasattr(runner, "writer")
    assert runner.writer is not None


def test_writer_is_async_generator():
    """Test that writer is an async generator function."""
    import inspect
    assert inspect.isasyncgenfunction(writer)


@pytest.mark.asyncio
async def test_writer_yields_integers():
    """Test that writer yields the expected number of integers."""
    desired = 5
    results = []
    async for item in writer(desired):
        results.append(item)

    assert len(results) == desired
    assert results == list(range(0, desired))


@pytest.mark.asyncio
async def test_writer_with_zero():
    """Test writer with zero items."""
    results = []
    async for item in writer(0):
        results.append(item)

    assert len(results) == 0


@pytest.mark.asyncio
async def test_writer_with_large_number():
    """Test writer with a larger number."""
    desired = 100
    results = []
    async for item in writer(desired):
        results.append(item)

    assert len(results) == desired
    assert results[0] == 0
    assert results[-1] == desired - 1


def test_reader_is_async():
    """Test that reader is an async function."""
    import inspect
    assert inspect.iscoroutinefunction(reader)


@pytest.mark.asyncio
async def test_reader_with_integer(capsys):
    """Test reader with an integer identifier."""
    await reader(42)
    captured = capsys.readouterr()
    assert "42" in captured.out


@pytest.mark.asyncio
async def test_reader_with_string(capsys):
    """Test reader with a string identifier."""
    await reader("test_value")
    captured = capsys.readouterr()
    assert "test_value" in captured.out


@pytest.mark.asyncio
async def test_reader_prints_output(capsys):
    """Test that reader prints its identifier."""
    test_id = "test_123"
    await reader(test_id)
    captured = capsys.readouterr()
    assert test_id in captured.out


def test_runner_configured_correctly():
    """Test that runner is configured with correct components."""
    # Verify runner has all required components
    assert runner.reader == reader
    assert runner.writer == writer


{%- if cookiecutter.include_aiocache == "y" %}


def test_cache_configuration_imported():
    """Test that cache configuration can be imported."""
    from {{cookiecutter.__package_slug}}.services.cache import configure_caches
    from {{cookiecutter.__package_slug}}.settings import settings

    assert configure_caches is not None
    assert settings is not None
{%- endif %}


def test_settings_has_project_name():
    """Test that settings has project_name for QuasiQueue."""
    from {{cookiecutter.__package_slug}}.settings import settings
    assert hasattr(settings, "project_name")
    assert settings.project_name == "{{cookiecutter.__package_slug}}"
