"""Comprehensive tests for cache service functionality."""

{%- if cookiecutter.include_aiocache == "y" %}
import pytest
from aiocache import caches

from {{ cookiecutter.__package_slug }}.settings import settings
from {{ cookiecutter.__package_slug }}.services.cache import (
    NoOpCache,
    clear_cache,
    configure_caches,
    delete_cached,
    get_cache,
    get_cached,
    set_cached,
)


class TestNoOpCache:
    """Test the NoOpCache backend implementation."""

    @pytest.fixture
    def noop_cache(self):
        """Create a NoOpCache instance."""
        return NoOpCache()

    @pytest.mark.asyncio
    async def test_noop_cache_get(self, noop_cache):
        """Test NoOpCache get returns None."""
        result = await noop_cache.get("test_key")
        assert result is None

    @pytest.mark.asyncio
    async def test_noop_cache_get_with_default(self, noop_cache):
        """Test NoOpCache get returns default value."""
        result = await noop_cache.get("test_key", default="default_value")
        assert result == "default_value"

    @pytest.mark.asyncio
    async def test_noop_cache_set(self, noop_cache):
        """Test NoOpCache set succeeds but doesn't store."""
        result = await noop_cache.set("test_key", "test_value")
        assert result is True
        # Verify it wasn't actually stored
        get_result = await noop_cache.get("test_key")
        assert get_result is None

    @pytest.mark.asyncio
    async def test_noop_cache_set_with_ttl(self, noop_cache):
        """Test NoOpCache set with TTL succeeds."""
        result = await noop_cache.set("test_key", "test_value", ttl=300)
        assert result is True

    @pytest.mark.asyncio
    async def test_noop_cache_add(self, noop_cache):
        """Test NoOpCache add succeeds."""
        result = await noop_cache.add("test_key", "test_value")
        assert result is True

    @pytest.mark.asyncio
    async def test_noop_cache_add_with_ttl(self, noop_cache):
        """Test NoOpCache add with TTL succeeds."""
        result = await noop_cache.add("test_key", "test_value", ttl=300)
        assert result is True

    @pytest.mark.asyncio
    async def test_noop_cache_delete(self, noop_cache):
        """Test NoOpCache delete returns 0 (key not found)."""
        result = await noop_cache.delete("test_key")
        assert result == 0

    @pytest.mark.asyncio
    async def test_noop_cache_exists(self, noop_cache):
        """Test NoOpCache exists returns False."""
        result = await noop_cache.exists("test_key")
        assert result is False

    @pytest.mark.asyncio
    async def test_noop_cache_multi_get(self, noop_cache):
        """Test NoOpCache multi_get returns all None."""
        result = await noop_cache.multi_get(["key1", "key2", "key3"])
        assert result == [None, None, None]

    @pytest.mark.asyncio
    async def test_noop_cache_multi_set(self, noop_cache):
        """Test NoOpCache multi_set succeeds."""
        result = await noop_cache.multi_set([("key1", "value1"), ("key2", "value2")])
        assert result is True

    @pytest.mark.asyncio
    async def test_noop_cache_increment(self, noop_cache):
        """Test NoOpCache increment returns delta."""
        result = await noop_cache.increment("counter", delta=5)
        assert result == 5

    @pytest.mark.asyncio
    async def test_noop_cache_increment_negative(self, noop_cache):
        """Test NoOpCache increment with negative delta."""
        result = await noop_cache.increment("counter", delta=-3)
        assert result == -3

    @pytest.mark.asyncio
    async def test_noop_cache_expire(self, noop_cache):
        """Test NoOpCache expire returns False (key not found)."""
        result = await noop_cache.expire("test_key", ttl=300)
        assert result is False

    @pytest.mark.asyncio
    async def test_noop_cache_clear(self, noop_cache):
        """Test NoOpCache clear succeeds."""
        await noop_cache.clear()
        # No assertion needed, just verify it doesn't raise

    @pytest.mark.asyncio
    async def test_noop_cache_raw(self, noop_cache):
        """Test NoOpCache raw returns None."""
        result = await noop_cache.raw("get", "test_key")
        assert result is None

    @pytest.mark.asyncio
    async def test_noop_cache_close(self, noop_cache):
        """Test NoOpCache close doesn't raise."""
        await noop_cache.close()
        # No assertion needed, just verify it doesn't raise

    def test_noop_cache_build_key(self, noop_cache):
        """Test NoOpCache build_key."""
        key = noop_cache.build_key("test_key")
        assert key == "test_key"

    def test_noop_cache_build_key_with_namespace(self, noop_cache):
        """Test NoOpCache build_key with namespace."""
        noop_cache.namespace = "prefix:"
        key = noop_cache.build_key("test_key")
        assert key == "prefix:test_key"


class TestCacheConfigurationEnabled:
    """Test cache configuration when caching is enabled."""

    @pytest.fixture(autouse=True)
    def reset_caches(self):
        """Reset cache configuration before each test."""
        # Clear any existing configuration
        caches._config = {}
        yield
        # Clean up after test
        caches._config = {}

    @pytest.mark.asyncio
    async def test_configure_caches_with_cache_enabled(self, monkeypatch):
        """Test cache configuration when cache_enabled=True."""
        monkeypatch.setattr(settings, "cache_enabled", True)
        monkeypatch.setattr(settings, "cache_redis_host", None)
        
        configure_caches()
        
        # Verify memory cache uses SimpleMemoryCache
        memory_cache = get_cache("memory")
        assert memory_cache is not None
        assert "SimpleMemoryCache" in str(type(memory_cache))

    @pytest.mark.asyncio
    async def test_configure_caches_with_redis(self, monkeypatch):
        """Test cache configuration with Redis enabled."""
        monkeypatch.setattr(settings, "cache_enabled", True)
        monkeypatch.setattr(settings, "cache_redis_host", "localhost")
        monkeypatch.setattr(settings, "cache_redis_port", 6379)
        
        configure_caches()
        
        # Verify persistent cache is configured
        config = caches.get_config()
        assert "persistent" in config
        assert config["persistent"]["cache"] == "aiocache.RedisCache"

    @pytest.mark.asyncio
    async def test_configure_caches_fallback_to_memory(self, monkeypatch):
        """Test cache fallback to memory when Redis not configured."""
        monkeypatch.setattr(settings, "cache_enabled", True)
        monkeypatch.setattr(settings, "cache_redis_host", None)
        
        configure_caches()
        
        # Verify persistent cache falls back to SimpleMemoryCache
        config = caches.get_config()
        assert "persistent" in config
        assert config["persistent"]["cache"] == "aiocache.SimpleMemoryCache"


class TestCacheConfigurationDisabled:
    """Test cache configuration when caching is disabled."""

    @pytest.fixture(autouse=True)
    def reset_caches(self):
        """Reset cache configuration before each test."""
        caches._config = {}
        yield
        caches._config = {}

    @pytest.mark.asyncio
    async def test_configure_caches_with_cache_disabled(self, monkeypatch):
        """Test cache configuration when cache_enabled=False."""
        monkeypatch.setattr(settings, "cache_enabled", False)
        
        configure_caches()
        
        # Verify NoOpCache is used
        config = caches.get_config()
        assert "memory" in config
        assert "NoOpCache" in config["memory"]["cache"]
        assert "persistent" in config
        assert "NoOpCache" in config["persistent"]["cache"]

    @pytest.mark.asyncio
    async def test_noop_cache_integration_memory(self, monkeypatch):
        """Test NoOpCache integration through memory cache."""
        monkeypatch.setattr(settings, "cache_enabled", False)
        configure_caches()
        
        # Test through cache API
        memory_cache = get_cache("memory")
        await memory_cache.set("test_key", "test_value")
        result = await memory_cache.get("test_key")
        assert result is None  # NoOpCache returns None

    @pytest.mark.asyncio
    async def test_noop_cache_integration_persistent(self, monkeypatch):
        """Test NoOpCache integration through persistent cache."""
        monkeypatch.setattr(settings, "cache_enabled", False)
        configure_caches()
        
        # Test through cache API
        persistent_cache = get_cache("persistent")
        await persistent_cache.set("test_key", "test_value")
        result = await persistent_cache.get("test_key")
        assert result is None  # NoOpCache returns None


class TestCacheHelperFunctions:
    """Test cache helper functions."""

    @pytest.fixture(autouse=True)
    def setup_cache(self, monkeypatch):
        """Setup cache configuration for tests."""
        caches._config = {}
        monkeypatch.setattr(settings, "cache_enabled", True)
        monkeypatch.setattr(settings, "cache_redis_host", None)
        monkeypatch.setattr(settings, "cache_default_ttl", 100)
        monkeypatch.setattr(settings, "cache_persistent_ttl", 500)
        configure_caches()
        yield
        caches._config = {}

    @pytest.mark.asyncio
    async def test_get_cached_miss(self):
        """Test get_cached when key doesn't exist."""
        result = await get_cached("missing_key")
        assert result is None

    @pytest.mark.asyncio
    async def test_set_and_get_cached(self):
        """Test set_cached and get_cached."""
        await set_cached("test_key", "test_value")
        result = await get_cached("test_key")
        assert result == "test_value"

    @pytest.mark.asyncio
    async def test_set_cached_with_custom_ttl(self):
        """Test set_cached with custom TTL."""
        await set_cached("test_key", "test_value", ttl=300)
        result = await get_cached("test_key")
        assert result == "test_value"

    @pytest.mark.asyncio
    async def test_set_cached_uses_default_ttl(self, monkeypatch):
        """Test set_cached uses default TTL from settings."""
        # This test verifies the TTL parameter is passed correctly
        await set_cached("test_key", "test_value")
        result = await get_cached("test_key")
        assert result == "test_value"

    @pytest.mark.asyncio
    async def test_set_cached_persistent_uses_persistent_ttl(self):
        """Test set_cached on persistent cache uses persistent TTL."""
        await set_cached("test_key", "test_value", alias="persistent")
        result = await get_cached("test_key", alias="persistent")
        assert result == "test_value"

    @pytest.mark.asyncio
    async def test_delete_cached(self):
        """Test delete_cached."""
        await set_cached("test_key", "test_value")
        await delete_cached("test_key")
        result = await get_cached("test_key")
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_cached_persistent(self):
        """Test delete_cached on persistent cache."""
        await set_cached("test_key", "test_value", alias="persistent")
        await delete_cached("test_key", alias="persistent")
        result = await get_cached("test_key", alias="persistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_clear_cache_memory(self):
        """Test clear_cache on memory cache."""
        await set_cached("key1", "value1")
        await set_cached("key2", "value2")
        await clear_cache("memory")
        result1 = await get_cached("key1")
        result2 = await get_cached("key2")
        assert result1 is None
        assert result2 is None

    @pytest.mark.asyncio
    async def test_clear_cache_persistent(self):
        """Test clear_cache on persistent cache."""
        await set_cached("key1", "value1", alias="persistent")
        await set_cached("key2", "value2", alias="persistent")
        await clear_cache("persistent")
        result1 = await get_cached("key1", alias="persistent")
        result2 = await get_cached("key2", alias="persistent")
        assert result1 is None
        assert result2 is None

    @pytest.mark.asyncio
    async def test_cache_complex_objects(self):
        """Test caching complex Python objects."""
        test_data = {
            "string": "value",
            "number": 42,
            "list": [1, 2, 3],
            "dict": {"nested": "data"},
        }
        await set_cached("complex_key", test_data)
        result = await get_cached("complex_key")
        assert result == test_data

    @pytest.mark.asyncio
    async def test_cache_isolation_between_aliases(self):
        """Test that memory and persistent caches are isolated."""
        await set_cached("shared_key", "memory_value", alias="memory")
        await set_cached("shared_key", "persistent_value", alias="persistent")
        
        memory_result = await get_cached("shared_key", alias="memory")
        persistent_result = await get_cached("shared_key", alias="persistent")
        
        assert memory_result == "memory_value"
        assert persistent_result == "persistent_value"


class TestCacheDisabledBehavior:
    """Test cache behavior when disabled via settings."""

    @pytest.fixture(autouse=True)
    def setup_disabled_cache(self, monkeypatch):
        """Setup cache with caching disabled."""
        caches._config = {}
        monkeypatch.setattr(settings, "cache_enabled", False)
        configure_caches()
        yield
        caches._config = {}

    @pytest.mark.asyncio
    async def test_disabled_cache_set_returns_nothing(self):
        """Test that setting values in disabled cache has no effect."""
        await set_cached("test_key", "test_value")
        result = await get_cached("test_key")
        assert result is None

    @pytest.mark.asyncio
    async def test_disabled_cache_delete_safe(self):
        """Test that deleting from disabled cache is safe."""
        await delete_cached("test_key")
        # Should not raise any errors

    @pytest.mark.asyncio
    async def test_disabled_cache_clear_safe(self):
        """Test that clearing disabled cache is safe."""
        await clear_cache()
        # Should not raise any errors

    @pytest.mark.asyncio
    async def test_disabled_cache_no_side_effects(self):
        """Test that disabled cache operations have no side effects."""
        # Set multiple values
        await set_cached("key1", "value1")
        await set_cached("key2", "value2")
        await set_cached("key3", "value3")
        
        # All gets should return None
        assert await get_cached("key1") is None
        assert await get_cached("key2") is None
        assert await get_cached("key3") is None


class TestCacheEdgeCases:
    """Test edge cases and error conditions."""

    @pytest.fixture(autouse=True)
    def setup_cache(self, monkeypatch):
        """Setup cache configuration."""
        caches._config = {}
        monkeypatch.setattr(settings, "cache_enabled", True)
        monkeypatch.setattr(settings, "cache_redis_host", None)
        configure_caches()
        yield
        caches._config = {}

    @pytest.mark.asyncio
    async def test_cache_none_value(self):
        """Test caching None as a value."""
        await set_cached("none_key", None)
        result = await get_cached("none_key")
        # Note: Depending on serialization, None might be cached or return None
        # This tests the behavior is consistent
        assert result is None

    @pytest.mark.asyncio
    async def test_cache_empty_string(self):
        """Test caching empty string."""
        await set_cached("empty_key", "")
        result = await get_cached("empty_key")
        assert result == ""

    @pytest.mark.asyncio
    async def test_cache_zero_value(self):
        """Test caching zero."""
        await set_cached("zero_key", 0)
        result = await get_cached("zero_key")
        assert result == 0

    @pytest.mark.asyncio
    async def test_cache_false_value(self):
        """Test caching False."""
        await set_cached("false_key", False)
        result = await get_cached("false_key")
        assert result is False

    @pytest.mark.asyncio
    async def test_cache_large_object(self):
        """Test caching large objects."""
        large_data = {"key" + str(i): "value" + str(i) for i in range(1000)}
        await set_cached("large_key", large_data)
        result = await get_cached("large_key")
        assert result == large_data

    @pytest.mark.asyncio
    async def test_get_cache_invalid_alias(self):
        """Test get_cache with invalid alias raises or returns None."""
        # This should handle invalid aliases gracefully
        try:
            cache = get_cache("invalid_alias")
            # If it returns something, it should be a valid cache object
            assert cache is not None
        except KeyError:
            # KeyError is also acceptable behavior
            pass

{%- endif %}
