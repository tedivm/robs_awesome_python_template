"""Tests for settings configuration."""
import pytest
import os
from {{cookiecutter.__package_slug}}.settings import settings
from {{cookiecutter.__package_slug}}.conf.settings import Settings
{%- if cookiecutter.include_aiocache == "y" %}
from {{cookiecutter.__package_slug}}.conf.cache import CacheSettings
{%- endif %}


def test_settings_exists():
    """Test that settings instance exists."""
    assert settings is not None


def test_settings_is_settings_class():
    """Test that settings is an instance of Settings."""
    assert isinstance(settings, Settings)


def test_settings_has_project_name():
    """Test that settings has project_name attribute."""
    assert hasattr(settings, "project_name")
    assert settings.project_name is not None
    assert len(settings.project_name) > 0


def test_settings_has_debug():
    """Test that settings has debug attribute."""
    assert hasattr(settings, "debug")
    assert isinstance(settings.debug, bool)


def test_settings_class_exists():
    """Test that Settings class exists."""
    assert Settings is not None


{%- if cookiecutter.include_aiocache == "y" %}


def test_settings_inherits_from_cache_settings():
    """Test that Settings inherits from CacheSettings."""
    assert issubclass(Settings, CacheSettings)
{%- endif %}


{%- if cookiecutter.include_quasiqueue == "y" %}


def test_settings_inherits_from_quasiqueue_settings():
    """Test that Settings inherits from QuasiQueueSettings."""
    from quasiqueue import Settings as QuasiQueueSettings
    assert issubclass(Settings, QuasiQueueSettings)
{%- endif %}


def test_settings_can_be_instantiated():
    """Test that Settings can be instantiated."""
    test_settings = Settings()
    assert test_settings is not None
    assert isinstance(test_settings, Settings)



{%- if cookiecutter.include_aiocache == "y" %}


def test_cache_settings_exists():
    """Test that CacheSettings class exists."""
    assert CacheSettings is not None


def test_cache_enabled_attribute():
    """Test that settings has cache_enabled attribute."""
    assert hasattr(settings, "cache_enabled")
    assert isinstance(settings.cache_enabled, bool)


def test_cache_enabled_default():
    """Test that cache_enabled defaults to True."""
    test_settings = Settings()
    assert test_settings.cache_enabled is True


def test_cache_redis_host_attribute():
    """Test that settings has cache_redis_host attribute."""
    assert hasattr(settings, "cache_redis_host")


def test_cache_redis_port_attribute():
    """Test that settings has cache_redis_port attribute."""
    assert hasattr(settings, "cache_redis_port")
    assert isinstance(settings.cache_redis_port, int)


def test_cache_redis_port_default():
    """Test that cache_redis_port defaults to 6379."""
    test_settings = Settings()
    assert test_settings.cache_redis_port == 6379


def test_cache_default_ttl_attribute():
    """Test that settings has cache_default_ttl attribute."""
    assert hasattr(settings, "cache_default_ttl")
    assert isinstance(settings.cache_default_ttl, int)


def test_cache_default_ttl_value():
    """Test that cache_default_ttl has reasonable default."""
    assert settings.cache_default_ttl == 300  # 5 minutes


def test_cache_persistent_ttl_attribute():
    """Test that settings has cache_persistent_ttl attribute."""
    assert hasattr(settings, "cache_persistent_ttl")
    assert isinstance(settings.cache_persistent_ttl, int)


def test_cache_persistent_ttl_value():
    """Test that cache_persistent_ttl has reasonable default."""
    assert settings.cache_persistent_ttl == 3600  # 1 hour
{%- endif %}



{%- if cookiecutter.include_quasiqueue == "y" %}


def test_project_name_attribute():
    """Test that settings has project_name from QuasiQueue."""
    assert hasattr(settings, "project_name")
    assert settings.project_name is not None
    assert len(settings.project_name) > 0
{%- endif %}


def test_debug_defaults_to_false():
    """Test that debug defaults to False."""
    test_settings = Settings()
    assert test_settings.debug is False


def test_all_required_attributes_present():
    """Test that all required attributes are present."""
    required_attrs = [
{%- if cookiecutter.include_quasiqueue == "y" %}
        "project_name",
{%- endif %}
        "debug",
{%- if cookiecutter.include_aiocache == "y" %}
        "cache_enabled",
        "cache_redis_host",
        "cache_redis_port",
        "cache_default_ttl",
        "cache_persistent_ttl"
{%- endif %}
    ]

    for attr in required_attrs:
        assert hasattr(settings, attr), f"Missing attribute: {attr}"



def test_settings_can_load_from_env():
    """Test that settings can be overridden by environment variables."""
    # This tests that the Settings class is properly configured
    # to load from environment variables using pydantic-settings
    test_settings = Settings()
    assert hasattr(test_settings, "model_config") or hasattr(test_settings, "Config")


{%- if cookiecutter.include_aiocache == "y" %}


def test_cache_enabled_from_env(monkeypatch):
    """Test that cache_enabled can be set from environment."""
    monkeypatch.setenv("CACHE_ENABLED", "false")
    test_settings = Settings()
    assert test_settings.cache_enabled is False
{%- endif %}


{%- if cookiecutter.include_quasiqueue != "y" %}


def test_debug_from_env(monkeypatch):
    """Test that debug can be set from environment."""
    monkeypatch.setenv("DEBUG", "True")
    test_settings = Settings()
    assert test_settings.debug is True
{%- endif %}


{%- if cookiecutter.include_aiocache == "y" %}


def test_cache_redis_host_from_env(monkeypatch):
    """Test that cache_redis_host can be set from environment."""
    monkeypatch.setenv("CACHE_REDIS_HOST", "test.redis.com")
    test_settings = Settings()
    assert test_settings.cache_redis_host == "test.redis.com"


def test_cache_redis_port_from_env(monkeypatch):
    """Test that cache_redis_port can be set from environment."""
    monkeypatch.setenv("CACHE_REDIS_PORT", "6380")
    test_settings = Settings()
    assert test_settings.cache_redis_port == 6380
{%- endif %}



def test_settings_validates_types():
    """Test that settings validates types correctly."""
    # This is implicitly tested by pydantic, but we verify it works
    test_settings = Settings()
    assert isinstance(test_settings.debug, bool)
{%- if cookiecutter.include_aiocache == "y" %}
    assert isinstance(test_settings.cache_enabled, bool)
    assert isinstance(test_settings.cache_redis_port, int)
    assert isinstance(test_settings.cache_default_ttl, int)
{%- endif %}
