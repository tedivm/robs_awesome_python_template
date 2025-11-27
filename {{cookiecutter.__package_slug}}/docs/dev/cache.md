# Caching

This project uses [aiocache](https://aiocache.readthedocs.io/) for caching, providing both in-memory and Redis-backed cache backends with full async/await support.

## Configuration

Caching is configured through the settings module with the following environment variables:

### Cache Control

- **CACHE_ENABLED**: Enable or disable caching (default: `True`)
  - When set to `False`, all cache operations become no-ops without requiring code changes

### Redis Configuration

- **CACHE_REDIS_HOST**: Redis hostname (default: `None`)
  - If not set, the persistent cache falls back to in-memory storage
- **CACHE_REDIS_PORT**: Redis port (default: `6379`)

### Default TTLs

- **CACHE_DEFAULT_TTL**: Default TTL for memory cache in seconds (default: `300` / 5 minutes)
- **CACHE_PERSISTENT_TTL**: Default TTL for persistent cache in seconds (default: `3600` / 1 hour)

## Cache Backends

Two cache backends are configured:

### Memory Cache

- **Alias**: `memory`
- **Implementation**: Always uses in-memory storage
- **Use case**: Fast, ephemeral caching for request-scoped or temporary data
- **Serializer**: Pickle
- **Default TTL**: 300 seconds (configurable via `CACHE_DEFAULT_TTL`)

### Persistent Cache

- **Alias**: `persistent`
- **Implementation**: Uses Redis if `CACHE_REDIS_HOST` is configured, otherwise falls back to in-memory
- **Use case**: Data that needs to persist across restarts or be shared across instances
- **Serializer**: Pickle
- **Default TTL**: 3600 seconds (configurable via `CACHE_PERSISTENT_TTL`)

## Usage

### Basic Cache Operations

```python
from {{cookiecutter.__package_slug}}.services.cache import get_cached, set_cached, delete_cached, clear_cache

# Get a cached value (uses memory cache by default)
value = await get_cached("my_key")

# Get from persistent cache
value = await get_cached("my_key", alias="persistent")

# Set a cached value with default TTL (5 minutes for memory cache)
await set_cached("my_key", "my_value")

# Set with custom TTL
await set_cached("my_key", "my_value", ttl=300, alias="persistent")

# Delete a cached value
await delete_cached("my_key", alias="persistent")

# Clear entire cache
await clear_cache(alias="persistent")
```

### Using Cache Decorators

You can use aiocache's built-in decorators directly:

```python
from aiocache import cached

@cached(ttl=600, alias="persistent", key_builder=lambda f, *args, **kwargs: f"user:{args[0]}")
async def get_user_data(user_id: int):
    # Expensive operation here
    return await fetch_user_from_database(user_id)
```

### Direct Cache Access

For more control, you can get a cache instance directly:

```python
from {{cookiecutter.__package_slug}}.services.cache import get_cache

# Get memory cache
cache = get_cache("memory")
await cache.set("key", "value", ttl=300)
value = await cache.get("key")

# Get persistent cache (Redis or fallback to memory)
cache = get_cache("persistent")
await cache.set("key", "value", ttl=3600)
value = await cache.get("key")
```

## Initialization

The cache system must be initialized before use.

{%- if cookiecutter.include_fastapi == "y" %}

### FastAPI

Caches are automatically initialized in the FastAPI startup event. No manual initialization is required.
{%- endif %}
{%- if cookiecutter.include_celery == "y" %}

### Celery

Caches are automatically initialized when Celery workers start. No manual initialization is required.
{%- endif %}
{%- if cookiecutter.include_quasiqueue == "y" %}

### QuasiQueue

Caches are automatically initialized when QuasiQueue starts via the main script. No manual initialization is required.
{%- endif %}

### Manual Initialization

If you need to initialize caches manually (e.g., in a custom script or CLI command), use:

```python
from {{cookiecutter.__package_slug}}.services.cache import configure_caches
from {{cookiecutter.__package_slug}}.settings import settings

configure_caches(settings)
```

## Best Practices

1. **Choose the right backend**:
   - Use `memory` cache for request-scoped or temporary data
   - Use `persistent` cache for data that needs to survive restarts or be shared across instances

2. **Set appropriate TTLs**:
   - Default TTLs are configured via settings and automatically applied
   - Override with custom TTLs only when needed
   - Shorter TTLs for frequently changing data, longer TTLs for stable data

3. **Use meaningful keys**:
   - Include version numbers or namespaces in cache keys to avoid conflicts
   - Example: `user:v1:123` instead of just `123`

4. **Handle cache misses**:
   - Always check if cached data is `None` and have a fallback mechanism
   - Cache operations are safe when caching is disabled

5. **Disable caching in development**:
   - Set `CACHE_ENABLED=False` to disable caching without code changes
   - Useful for debugging or testing uncached behavior

6. **Monitor cache size**:
   - Redis caches can grow large; implement eviction policies and monitor memory usage
   - Use appropriate TTLs to prevent unbounded growth

## Development vs Production

Configure caching behavior through environment variables:

### Development

```bash
# Disable caching entirely for debugging
export CACHE_ENABLED=False

# Or use caching without Redis (both backends use memory)
export CACHE_REDIS_HOST=
export CACHE_DEFAULT_TTL=60
export CACHE_PERSISTENT_TTL=300

# Or use local Redis
export CACHE_REDIS_HOST=localhost
export CACHE_REDIS_PORT=6379
```

### Production

```bash
# Enable caching with Redis
export CACHE_ENABLED=True
export CACHE_REDIS_HOST=redis-cluster
export CACHE_REDIS_PORT=6379
export CACHE_DEFAULT_TTL=300
export CACHE_PERSISTENT_TTL=3600
```

## Disabling Caches

To disable caching without changing code:

1. **Via Environment Variable**: Set `CACHE_ENABLED=False`
2. **Result**: All cache operations (get, set, delete, clear) become no-ops
3. **Use Cases**:
   - Debugging issues related to stale cache data
   - Testing application behavior without caching
   - Temporary troubleshooting in production

When caching is disabled, your application continues to work normally - cache operations simply don't store or retrieve any data.

## References

- [aiocache Documentation](https://aiocache.readthedocs.io/)
- [Redis Best Practices](https://redis.io/docs/manual/patterns/)
