---
name: aiocache
description: "Configure or use the aiocache caching layer. Use when: adding cache reads/writes, configuring cache backends, working with TTLs, enabling/disabling caching, or understanding the NoOpCache fallback pattern."
---

# aiocache Caching

> **context7**: If the `context7` tools are available, resolve and load the full `aiocache` documentation before making changes:
> ```
> context7_resolve-library-id: "aiocache"
> context7_query-docs: /aio-libs/aiocache
> ```

The caching layer is defined in `{{cookiecutter.__package_slug}}/services/cache.py`. It provides helper functions and a `NoOpCache` fallback for when caching is disabled.

---

## Cache Aliases

Three cache backends are configured by `configure_caches()`:

| Alias         | Backend                         | Default TTL       |
| ------------- | ------------------------------- | ----------------- |
| `memory`      | Always in-memory                | `cache_default_ttl` (300s) |
| `persistent`  | Redis if configured, else memory | `cache_persistent_ttl` (3600s) |
| `default`     | Same as `memory`                | `cache_persistent_ttl` (3600s)* |

\* *Note: `set_cached()` applies `cache_default_ttl` only when `alias == "memory"`, so `default` falls through to `cache_persistent_ttl`.*

---

## Using the Helpers

```python
from {{cookiecutter.__package_slug}}.services.cache import get_cached, set_cached, delete_cached, clear_cache

# Get (returns None on miss)
value = await get_cached("user:123")

# Set with default TTL
await set_cached("user:123", user_data)

# Set with custom TTL
await set_cached("user:123", user_data, ttl=600, alias="persistent")

# Delete
await delete_cached("user:123", alias="persistent")

# Clear entire cache
await clear_cache(alias="persistent")
```

---

## Direct Cache Access

For operations not covered by the helpers:

```python
from {{cookiecutter.__package_slug}}.services.cache import get_cache

cache = get_cache("memory")
exists = await cache.exists("key")
```

---

## Cache Decorator

Use `@cached` to automatically cache function return values. The decorator takes a cache **instance** (not an alias string) as its first argument. Retrieve the instance with `get_cache()`:

```python
from aiocache import cached
from {{cookiecutter.__package_slug}}.services.cache import get_cache

@cached(get_cache("memory"), ttl=300, key_builder=lambda f, *args, **kwargs: f"user:{args[0]}")
async def get_user(user_id: int) -> dict[str, str] | None:
    # Expensive DB call — cached for 300s
    return await fetch_user_from_db(user_id)
```

**Decorator parameters:**
- **First positional arg**: cache instance from `get_cache(alias)` — required
- **`ttl`**: time-to-live in seconds (default: 60)
- **`key`**: static cache key (overrides `key_builder` if set)
- **`key_builder`**: callable that generates the cache key. Signature: `lambda f, *args, **kwargs: str`
- **`noself=True`**: use on class methods to share the cache across instances

**Default key format:** `namespace__module__func_name(args)[kwargs]` — e.g., `api__main__fetch_user(1,)[]`

**Key builder patterns:**

```python
# Default key builder (uses function name + args)
@cached(get_cache("memory"), ttl=300)

# Static key (no key_builder needed)
@cached(get_cache("memory"), ttl=300, key="singleton:config")

# Custom key with positional arg
@cached(get_cache("memory"), ttl=300, key_builder=lambda f, *args, **kwargs: f"user:{args[0]}")

# Custom key with keyword arg
@cached(get_cache("memory"), ttl=300, key_builder=lambda f, *args, **kwargs: f"config:{kwargs.get('name')}")

# Hashed key for complex arguments
import hashlib
def hash_key_builder(f, *args, **kwargs):
    key = f"{f.__name__}:{args}:{sorted(kwargs.items())}"
    return hashlib.md5(key.encode()).hexdigest()

@cached(get_cache("memory"), ttl=300, key_builder=hash_key_builder)
async def search_products(query: str, category: str | None = None, page: int = 1) -> list[str]:
    ...
```

**Bypassing the cache on individual calls:**

```python
# Skip cache read (always execute function)
result = await get_user(1, cache_read=False)

# Skip cache write (don't store result)
result = await get_user(2, cache_write=False)

# Non-blocking write (don't wait for cache to accept)
result = await get_user(3, aiocache_wait_for_write=False)
```

---

## Multi-Cache Decorator

Use `@multi_cached` for functions that return dicts and need to cache individual keys. On subsequent calls, only missing keys are fetched:

```python
from aiocache import multi_cached
from {{cookiecutter.__package_slug}}.services.cache import get_cache

@multi_cached(get_cache("memory"), keys_from_attr="user_ids", ttl=300)
async def get_users(user_ids: list[int]) -> dict[int, dict[str, str]]:
    # Only uncached user_ids will be passed here on subsequent calls
    return {uid: {"id": uid, "name": f"User {uid}"} for uid in user_ids}

# With custom key builder
@multi_cached(
    get_cache("persistent"),
    keys_from_attr="product_ids",
    key_builder=lambda key, f, *args, **kwargs: f"product:{key}",
    ttl=3600
)
async def get_products(product_ids: list[str]) -> dict[str, dict[str, str]]:
    ...

# Skip caching for certain values
@multi_cached(
    get_cache("memory"),
    keys_from_attr="ids",
    skip_cache_func=lambda key, value: value is None or value.get("inactive"),
    ttl=300
)
async def get_accounts(ids: list[str]) -> dict[str, dict[str, str] | None]:
    ...
```

**`@multi_cached` parameters:**
- **First positional arg**: cache instance from `get_cache(alias)` — required
- **`keys_from_attr`**: name of the argument containing the list of keys to cache
- **`ttl`**: time-to-live in seconds (default: 60)
- **`key_builder`**: callable for custom key generation. Signature: `lambda key, func, *args, **kwargs: str`
- **`skip_cache_func`**: callable to skip caching specific values. Signature: `lambda key, value: bool`

---

## Initialization

Caches are automatically initialized by:
- FastAPI lifespan event (on startup)
- Celery `on_after_configure` signal
- QuasiQueue main entry point

For custom scripts or CLI commands, call manually:

```python
from {{cookiecutter.__package_slug}}.services.cache import configure_caches
configure_caches()
```

---

## NoOpCache

When `CACHE_ENABLED=False`, all caches use `NoOpCache` — a transparent drop-in that satisfies the `BaseCache` interface without storing anything. This means code that uses the cache helpers works identically whether caching is enabled or not.

---

## Key Conventions

- Use meaningful, namespaced keys: `user:v1:123` not just `123`
- Always check for `None` returns — cache misses are normal
- Use `memory` for request-scoped data, `persistent` for cross-instance sharing
- Set `CACHE_ENABLED=False` in development to debug uncached behavior

---

## Style Checklist

- [ ] Cache keys use namespaced format (`entity:version:id`)
- [ ] Cache miss returns `None` — always have a fallback
- [ ] `configure_caches()` called before any cache operations in custom scripts
- [ ] `memory` alias for ephemeral data, `persistent` for shared data
- [ ] TTL explicitly set only when different from defaults
- [ ] `@cached` decorator receives a cache instance from `get_cache()`, not an alias string
- [ ] `@cached` only used on `async` functions — never synchronous
- [ ] `noself=True` set on class method decorators
- [ ] `@multi_cached` used for functions returning dicts of individually-cached items
- [ ] `skip_cache_func` set on `@multi_cached` to avoid caching None/inactive values

---

## Further Reading

- [docs/dev/cache.md](../../docs/dev/cache.md) — Full caching developer guide
- [aiocache Docs](https://aiocache.readthedocs.io/)
