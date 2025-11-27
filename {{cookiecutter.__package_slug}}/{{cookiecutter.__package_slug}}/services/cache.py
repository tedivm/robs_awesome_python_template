"""Cache service configuration and utilities for {{ cookiecutter.package_name }}."""

from typing import Any

from aiocache import caches  # type: ignore[import-untyped]
from aiocache.base import BaseCache  # type: ignore[import-untyped]

from ..settings import settings


class NoOpCache(BaseCache):
    """
    A no-operation cache that does nothing.

    This cache backend is used when caching is disabled via settings.cache_enabled.
    It extends aiocache's BaseCache to provide a transparent drop-in replacement
    that performs no actual caching operations.

    All operations return values that indicate success without performing any
    actual caching, making this a true no-op implementation that satisfies the
    aiocache BaseCache interface.
    """

    NAME = "noop"

    def build_key(self, key: str, namespace: str | None = None) -> str:
        """Build a cache key using the standard string builder."""
        return self._str_build_key(key, namespace)  # type: ignore[no-any-return]

    async def _add(self, key: str, value: Any, ttl: int | float | None, _conn: Any = None) -> bool:
        """
        No-op add operation.

        Returns True to indicate the key was "added" successfully.
        """
        return True

    async def _get(self, key: str, encoding: str, _conn: Any = None) -> bytes | None:
        """
        No-op get operation.

        Always returns None to indicate the key doesn't exist.
        """
        return None

    async def _gets(self, key: str, encoding: str = "utf-8", _conn: Any = None) -> bytes | None:
        """
        No-op gets operation (get with CAS token).

        Always returns None to indicate the key doesn't exist.
        """
        return None

    async def _multi_get(self, keys: list[str], encoding: str, _conn: Any = None) -> list[bytes | None]:
        """
        No-op multi-get operation.

        Returns a list of None values matching the number of requested keys.
        """
        return [None] * len(keys)

    async def _set(
        self, key: str, value: Any, ttl: int | float | None, _cas_token: Any = None, _conn: Any = None
    ) -> bool:
        """
        No-op set operation.

        Returns True to indicate the key was "set" successfully.
        """
        return True

    async def _multi_set(
        self, pairs: list[tuple[str, Any]], ttl: int | float | None, _conn: Any = None
    ) -> bool:
        """
        No-op multi-set operation.

        Returns True to indicate all keys were "set" successfully.
        """
        return True

    async def _delete(self, key: str, _conn: Any = None) -> int:
        """
        No-op delete operation.

        Returns 0 to indicate no keys were deleted (key didn't exist).
        """
        return 0

    async def _exists(self, key: str, _conn: Any = None) -> bool:
        """
        No-op exists operation.

        Always returns False to indicate the key doesn't exist.
        """
        return False

    async def _increment(self, key: str, delta: int, _conn: Any = None) -> int:
        """
        No-op increment operation.

        Returns the delta value as if the key didn't exist and was created with that value.
        """
        return delta

    async def _expire(self, key: str, ttl: int | float, _conn: Any = None) -> bool:
        """
        No-op expire operation.

        Returns False to indicate the key doesn't exist.
        """
        return False

    async def _clear(self, namespace: str | None, _conn: Any = None) -> bool:
        """
        No-op clear operation.

        Returns True to indicate the namespace was "cleared" successfully.
        """
        return True

    async def _raw(self, command: str, *args: Any, **kwargs: Any) -> Any:
        """
        No-op raw operation.

        Returns None as there's no underlying client to execute commands.
        """
        return None

    async def _close(self, *args: Any, _conn: Any = None, **kwargs: Any) -> None:
        """No-op close operation - nothing to close."""
        pass


def configure_caches() -> None:
    """Configure aiocache with memory and persistent backends."""
    cache_config = {
        "default": {
            "cache": "aiocache.SimpleMemoryCache" if settings.cache_enabled else f"{__name__}.NoOpCache",
            "serializer": {"class": "aiocache.serializers.PickleSerializer"},
        },
        "memory": {
            "cache": "aiocache.SimpleMemoryCache" if settings.cache_enabled else f"{__name__}.NoOpCache",
            "serializer": {"class": "aiocache.serializers.PickleSerializer"},
        },
    }

    # Use Redis for persistent cache if configured, otherwise fall back to memory
    if not settings.cache_enabled:
        cache_config["persistent"] = {
            "cache": f"{__name__}.NoOpCache",
            "serializer": {"class": "aiocache.serializers.PickleSerializer"},
        }
    elif settings.cache_redis_host:
        cache_config["persistent"] = {
            "cache": "aiocache.RedisCache",
            "endpoint": settings.cache_redis_host,
            "port": str(settings.cache_redis_port),
            "serializer": {"class": "aiocache.serializers.PickleSerializer"},
        }
    else:
        cache_config["persistent"] = {
            "cache": "aiocache.SimpleMemoryCache",
            "serializer": {"class": "aiocache.serializers.PickleSerializer"},
        }

    caches.set_config(cache_config)


def get_cache(alias: str = "memory") -> BaseCache:
    """
    Get a configured cache instance.

    Args:
        alias: Cache alias to retrieve. Options are "memory" (default) or "persistent".
               "memory" is always in-memory. "persistent" uses Redis if configured,
               otherwise falls back to in-memory.

    Returns:
        Configured Cache instance
    """
    return caches.get(alias)


async def get_cached(key: str, alias: str = "memory") -> Any | None:
    """
    Get a value from cache.

    Args:
        key: Cache key
        alias: Cache alias to use ("memory" or "persistent")

    Returns:
        Cached value or None if not found
    """
    cache = get_cache(alias)
    return await cache.get(key)


async def set_cached(key: str, value: Any, ttl: int | None = None, alias: str = "memory") -> None:
    """
    Set a value in cache.

    Args:
        key: Cache key
        value: Value to cache
        ttl: Time to live in seconds. If None, uses default TTL based on cache alias.
        alias: Cache alias to use ("memory" or "persistent")
    """
    if ttl is None:
        ttl = settings.cache_default_ttl if alias == "memory" else settings.cache_persistent_ttl

    cache = get_cache(alias)
    await cache.set(key, value, ttl=ttl)


async def delete_cached(key: str, alias: str = "memory") -> None:
    """
    Delete a value from cache.

    Args:
        key: Cache key
        alias: Cache alias to use ("memory" or "persistent")
    """
    cache = get_cache(alias)
    await cache.delete(key)


async def clear_cache(alias: str = "memory") -> None:
    """
    Clear all values from cache.

    Args:
        alias: Cache alias to use ("memory" or "persistent")
    """
    cache = get_cache(alias)
    await cache.clear()
