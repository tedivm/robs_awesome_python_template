from pydantic_settings import BaseSettings


class CacheSettings(BaseSettings):
    # Cache control
    cache_enabled: bool = True

    # Redis configuration
    cache_redis_host: str | None = None
    cache_redis_port: int = 6379

    # Default TTLs (in seconds)
    cache_default_ttl: int = 300  # 5 minutes for memory cache
    cache_persistent_ttl: int = 3600  # 1 hour for persistent cache
