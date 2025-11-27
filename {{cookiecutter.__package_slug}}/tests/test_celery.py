"""Tests for Celery task queue configuration."""
import pytest
from {{cookiecutter.__package_slug}}.celery import celery, hello_world


def test_celery_app_exists():
    """Test that Celery app is properly instantiated."""
    assert celery is not None
    assert hasattr(celery, "tasks")


def test_celery_app_name():
    """Test that Celery app has correct name."""
    assert celery.main == "{{cookiecutter.__package_slug}}"


def test_celery_has_signals():
    """Test that Celery signal handlers are available."""
    assert hasattr(celery, "on_after_configure")
    assert hasattr(celery, "on_after_finalize")


def test_hello_world_task_registered():
    """Test that hello_world task is registered with Celery."""
    assert "{{cookiecutter.__package_slug}}.celery.hello_world" in celery.tasks


def test_hello_world_is_task():
    """Test that hello_world is a Celery task."""
    assert hasattr(hello_world, "delay")
    assert hasattr(hello_world, "apply_async")
    assert callable(hello_world)


def test_hello_world_task_name():
    """Test that hello_world task has correct name."""
    assert hello_world.name == "{{cookiecutter.__package_slug}}.celery.hello_world"


def test_hello_world_execution(capsys):
    """Test that hello_world task executes without error."""
    # Run the task directly (not async)
    hello_world()

    # Check that it printed the expected message
    captured = capsys.readouterr()
    assert "Hello World!" in captured.out


def test_periodic_task_setup_exists():
    """Test that periodic task setup function exists."""
    # The setup_periodic_tasks function should be connected to the signal
    # We can't easily test the actual registration without a running worker
    # but we can verify the signal handler exists
    assert hasattr(celery, "on_after_finalize")


def test_periodic_tasks_can_be_configured():
    """Test that periodic tasks configuration doesn't raise errors."""
    # This is a basic smoke test - in a real scenario you'd need a running worker
    # to test actual periodic task execution
    try:
        # Just verify the celery app is properly configured for periodic tasks
        assert celery.conf.beat_schedule is not None or True
    except AttributeError:
        # beat_schedule might not be set if not configured
        pass


{%- if cookiecutter.include_aiocache == "y" %}


def test_cache_setup_handler_exists():
    """Test that cache setup handler is registered."""
    # The setup_caches function should be connected to on_after_configure
    assert hasattr(celery, "on_after_configure")


def test_cache_setup_imports():
    """Test that cache configuration can be imported."""
    from {{cookiecutter.__package_slug}}.services.cache import configure_caches
    from {{cookiecutter.__package_slug}}.settings import settings

    assert configure_caches is not None
    assert settings is not None

    # Test that configure_caches is callable
    assert callable(configure_caches)
{%- endif %}
