# Settings

This project uses [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) for configuration management, providing type-safe settings with environment variable support and validation.

## Configuration Structure

The settings system is organized into multiple modules:

- **`{{cookiecutter.__package_slug}}/conf/settings.py`**: Main Settings class
{%- if cookiecutter.include_aiocache == "y" %}
- **`{{cookiecutter.__package_slug}}/conf/cache.py`**: Cache-specific settings
{%- endif %}
{%- if cookiecutter.include_sqlalchemy == "y" %}
- **`{{cookiecutter.__package_slug}}/conf/db.py`**: Database settings
{%- endif %}
- **`{{cookiecutter.__package_slug}}/settings.py`**: Global settings instance

## Accessing Settings

### Global Settings Instance

A pre-configured settings instance is available throughout the application:

```python
from {{cookiecutter.__package_slug}}.conf import settings

# Access settings
print(settings.project_name)
print(settings.debug)
print(settings.database_url)
```

### In Different Components

{%- if cookiecutter.include_fastapi == "y" %}

**FastAPI Routes**:

```python
from {{cookiecutter.__package_slug}}.conf import settings
from fastapi import APIRouter

router = APIRouter()

@router.get("/config")
async def get_config():
    return {
        "project": settings.project_name,
        "debug": settings.debug,
    }
```

{%- endif %}
{%- if cookiecutter.include_celery == "y" %}

**Celery Tasks**:

```python
from {{cookiecutter.__package_slug}}.conf import settings
from {{cookiecutter.__package_slug}}.celery import celery

@celery.task
def example_task():
    # Note: Celery configuration (broker, backend) is NOT in Settings
    # Use settings for application-specific configuration only
    project_name = settings.project_name
    # Task logic here
```

{%- endif %}
{%- if cookiecutter.include_cli == "y" %}

**CLI Commands**:

```python
from {{cookiecutter.__package_slug}}.conf import settings
from {{cookiecutter.__package_slug}}.cli import app

@app.command()
def show_config():
    """Display current configuration."""
    print(f"Project: {settings.project_name}")
    print(f"Debug: {settings.debug}")
```

{%- endif %}

## Environment Variables

### Setting Values

Configure the application using environment variables:

```bash
# Set environment variables
export PROJECT_NAME="My Application"
export DEBUG="True"
export DATABASE_URL="postgresql+asyncpg://user:pass@localhost/mydb"

# Or use a .env file
echo 'PROJECT_NAME="My Application"' > .env
echo 'DEBUG=True' >> .env
echo 'DATABASE_URL="postgresql+asyncpg://user:pass@localhost/mydb"' >> .env
```

### Loading from .env Files

The settings system automatically loads from `.env` files in the project root:

```python
# {{cookiecutter.__package_slug}}/conf/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
```

### Environment Variable Prefixes

To avoid conflicts, you can add a prefix to all environment variables:

```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MYAPP_",  # Now use MYAPP_DEBUG instead of DEBUG
    )

    debug: bool = False
```

## Core Settings

### Default Settings

The base Settings class includes:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application
    project_name: str = "{{cookiecutter.__package_slug}}"
    version: str = "0.1.0"
    debug: bool = False
{%- if cookiecutter.include_sqlalchemy == "y" %}

    # Database
    database_url: str = "postgresql+asyncpg://user:pass@localhost/db"
{%- endif %}
{%- if cookiecutter.include_aiocache == "y" %}

    # Cache
    cache_backend: str = "memory"
    redis_url: str = "redis://localhost:6379/0"
{%- endif %}
{%- if cookiecutter.include_quasiqueue == "y" %}

    # QuasiQueue settings come from QuasiQueueSettings base class
{%- endif %}
```

{%- if cookiecutter.include_celery == "y" %}

**Note**: Celery does NOT use the Settings class. Celery must be configured using environment variables (prefixed with `CELERY_`), a `celeryconfig.py` file, or programmatically. See the [Celery documentation](celery.md) for details.
{%- endif %}

## Adding Custom Settings

### Simple Settings

Add new fields to the Settings class:

```python
# {{cookiecutter.__package_slug}}/conf/settings.py
from pydantic import SecretStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Existing settings...

    # Add new settings
    max_upload_size: int = 10_000_000  # 10MB default
    allowed_hosts: list[str] = ["localhost", "127.0.0.1"]
    api_key: SecretStr = SecretStr("")  # Use SecretStr for secrets

    model_config = SettingsConfigDict(
        env_file=".env",
    )
```

Usage:

```bash
export MAX_UPLOAD_SIZE="20000000"
export ALLOWED_HOSTS='["example.com", "api.example.com"]'
export API_KEY="secret-key-here"
```

**Note**: Use `SecretStr` for sensitive values like passwords, API keys, and tokens. This prevents secrets from being accidentally logged or exposed:

```python
from pydantic import SecretStr

class Settings(BaseSettings):
    api_key: SecretStr
    database_password: SecretStr

# Access the secret value when needed
settings.api_key.get_secret_value()  # Returns the actual string
print(settings.api_key)  # Prints: **********
```

### Nested Settings

Organize related settings into nested models:

```python
from pydantic import BaseModel
from pydantic_settings import BaseSettings

class EmailSettings(BaseModel):
    smtp_host: str = "localhost"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    from_address: str = "noreply@example.com"

class Settings(BaseSettings):
    project_name: str = "{{cookiecutter.__package_slug}}"

    # Nested settings
    email: EmailSettings = EmailSettings()
```

Usage:

```bash
export EMAIL__SMTP_HOST="smtp.gmail.com"  # Double underscore for nested
export EMAIL__SMTP_PORT="587"
export EMAIL__FROM_ADDRESS="noreply@myapp.com"
```

Access nested settings:

```python
from {{cookiecutter.__package_slug}}.conf import settings

print(settings.email.smtp_host)
print(settings.email.from_address)
```

### Computed Properties

Add derived values using properties:

```python
class Settings(BaseSettings):
    debug: bool = False
    database_url: str = "postgresql+asyncpg://localhost/db"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.debug

    @property
    def database_name(self) -> str:
        """Extract database name from URL."""
        # Parse database_url and return database name
        return self.database_url.split("/")[-1]
```

## Validation

### Type Validation

Pydantic automatically validates types:

```python
class Settings(BaseSettings):
    port: int = 8000
    timeout: float = 30.0
    debug: bool = False
    allowed_hosts: list[str] = []
```

Invalid values raise validation errors:

```bash
export PORT="not-a-number"  # Raises ValidationError
```

### Custom Validators

Add custom validation logic:

```python
from pydantic import field_validator, BaseSettings

class Settings(BaseSettings):
    port: int = 8000
    database_url: str = ""

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        if not 1 <= v <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return v

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError("Database URL must use PostgreSQL")
        return v
```

### Required Settings

Mark settings as required by not providing defaults:

```python
class Settings(BaseSettings):
    # Required - will raise error if not provided
    api_key: str
    database_url: str

    # Optional - has default
    debug: bool = False
```

## Conditional Settings

### Feature-Based Configuration

Load different settings based on enabled features:

```python
from typing import Optional

class Settings(BaseSettings):
    # Core settings
    project_name: str = "{{cookiecutter.__package_slug}}"
    debug: bool = False

    # Optional feature settings
    database_url: Optional[str] = None
    redis_url: Optional[str] = None

    @property
    def has_database(self) -> bool:
        return self.database_url is not None

    @property
    def has_cache(self) -> bool:
        return self.redis_url is not None
```

**Note**: In the actual template, optional features like database and cache settings are added via inheritance from specialized settings classes (e.g., `DatabaseSettings`, `CacheSettings`) only when those features are enabled.

### Environment-Specific Settings

Use different settings per environment:

```python
from enum import Enum

class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class Settings(BaseSettings):
    environment: Environment = Environment.DEVELOPMENT
    debug: bool = False

    @property
    def is_production(self) -> bool:
        return self.environment == Environment.PRODUCTION

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Auto-set debug based on environment
        if self.environment != Environment.PRODUCTION:
            self.debug = True
```

## Multiple Settings Files

### Environment-Specific Files

Load different .env files per environment:

```python
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# Determine environment
env = os.getenv("ENVIRONMENT", "development")
env_file = f".env.{env}"  # .env.development, .env.production, etc.

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
    )
```

Project structure:

```
.env                 # Default settings
.env.development     # Development overrides
.env.staging         # Staging overrides
.env.production      # Production overrides
```

## Testing with Settings

### Testing Settings Existence

Test that settings are properly instantiated and accessible:

```python
# tests/test_settings.py
from {{cookiecutter.__package_slug}}.settings import settings
from {{cookiecutter.__package_slug}}.conf.settings import Settings


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
```

### Testing Settings Inheritance

Test that Settings properly inherits from base classes:

```python
from {{cookiecutter.__package_slug}}.conf.cache import CacheSettings


def test_settings_inherits_from_cache_settings():
    """Test that Settings inherits from CacheSettings."""
    assert issubclass(Settings, CacheSettings)


def test_settings_inherits_from_quasiqueue_settings():
    """Test that Settings inherits from QuasiQueueSettings."""
    from quasiqueue import Settings as QuasiQueueSettings
    assert issubclass(Settings, QuasiQueueSettings)
```

### Testing Settings Instantiation

Test that Settings can be created and configured:

```python
def test_settings_can_be_instantiated():
    """Test that Settings can be instantiated."""
    test_settings = Settings()
    assert test_settings is not None
    assert isinstance(test_settings, Settings)


def test_settings_has_defaults():
    """Test that settings have default values."""
    test_settings = Settings()
    assert hasattr(test_settings, "project_name")
    assert hasattr(test_settings, "debug")
```

### Override Settings with Monkeypatch

Use pytest's `monkeypatch` to override environment variables:

```python
def test_debug_from_env(monkeypatch):
    """Test that DEBUG setting can be set from environment."""
    monkeypatch.setenv("DEBUG", "True")

    # Create new settings instance to pick up env var
    test_settings = Settings()
    assert test_settings.debug is True


def test_project_name_from_env(monkeypatch):
    """Test that PROJECT_NAME can be overridden."""
    monkeypatch.setenv("PROJECT_NAME", "Test Project")

    test_settings = Settings()
    assert test_settings.project_name == "Test Project"


def test_database_url_from_env(monkeypatch):
    """Test database URL configuration."""
    test_url = "postgresql+asyncpg://test:pass@localhost/testdb"
    monkeypatch.setenv("DATABASE_URL", test_url)

    test_settings = Settings()
    assert test_settings.database_url == test_url
```

### Testing Cache Configuration

Test cache-related settings when cache is enabled:

```python
def test_cache_configuration_exists():
    """Test that cache configuration is present."""
    from {{cookiecutter.__package_slug}}.conf.cache import CacheSettings

    cache_settings = CacheSettings()
    assert hasattr(cache_settings, "cache_backend")


def test_cache_backend_setting(monkeypatch):
    """Test cache backend configuration."""
    monkeypatch.setenv("CACHE_BACKEND", "redis")

    test_settings = Settings()
    assert test_settings.cache_backend == "redis"


def test_redis_url_setting(monkeypatch):
    """Test Redis URL configuration."""
    redis_url = "redis://localhost:6379/1"
    monkeypatch.setenv("REDIS_URL", redis_url)

    test_settings = Settings()
    assert test_settings.redis_url == redis_url
```

### Test Fixtures for Settings

Create reusable fixtures for common test scenarios:

```python
import pytest


@pytest.fixture
def test_settings(monkeypatch):
    """Provide settings configured for testing."""
    monkeypatch.setenv("DEBUG", "True")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///test.db")
    monkeypatch.setenv("CACHE_BACKEND", "memory")

    from {{cookiecutter.__package_slug}}.conf.settings import Settings
    return Settings()


@pytest.fixture
def production_settings(monkeypatch):
    """Provide settings configured for production."""
    monkeypatch.setenv("DEBUG", "False")
    monkeypatch.setenv("DATABASE_URL", "postgresql://prod/db")

    from {{cookiecutter.__package_slug}}.conf.settings import Settings
    return Settings()


def test_with_test_settings(test_settings):
    """Test using the test_settings fixture."""
    assert test_settings.debug is True
    assert "sqlite" in test_settings.database_url


def test_with_production_settings(production_settings):
    """Test using the production_settings fixture."""
    assert production_settings.debug is False
```

### Testing Optional Features

Test that settings handle optional features correctly:

```python
def test_settings_with_all_features():
    """Test settings when all features are enabled."""
    test_settings = Settings()

    # Check that all feature-related settings exist
    # (based on which features are enabled in the template)
    if hasattr(test_settings, "database_url"):
        assert test_settings.database_url is not None
    if hasattr(test_settings, "cache_backend"):
        assert test_settings.cache_backend in ["memory", "redis"]


def test_cache_settings_conditional():
    """Test cache settings are available when cache is enabled."""
    from {{cookiecutter.__package_slug}}.conf import settings

    if hasattr(settings, "cache_backend"):
        assert settings.cache_backend in ["memory", "redis"]
```

## Best Practices

1. **Use Type Hints**: Always provide type hints for settings - enables IDE autocomplete and validation:

   ```python
   port: int = 8000  # Good
   port = 8000       # Bad - no type checking
   ```

2. **Use SecretStr for Sensitive Data**: Protect passwords, API keys, tokens, and other secrets from accidental exposure:

   ```python
   from pydantic import SecretStr

   class Settings(BaseSettings):
       api_key: SecretStr              # Good - prevents logging secrets
       database_password: SecretStr    # Good
       jwt_secret: SecretStr           # Good

       # api_key: str                  # Bad - secret can be logged

   # Access when needed
   actual_key = settings.api_key.get_secret_value()
   ```

   Benefits of `SecretStr`:
   - Prevents secrets from appearing in logs
   - Hides values in error messages and tracebacks
   - Shows `**********` when printed or serialized
   - Makes it explicit which fields contain sensitive data

3. **Provide Sensible Defaults**: Set reasonable defaults for all optional settings

4. **Document Settings**: Add docstrings to explain each setting:

   ```python
   class Settings(BaseSettings):
       max_connections: int = 10
       """Maximum number of concurrent database connections."""

       timeout: float = 30.0
       """Request timeout in seconds."""
   ```

5. **Group Related Settings**: Use nested models to organize related configuration

6. **Validate Early**: Use validators to catch configuration errors at startup rather than runtime

7. **Keep Secrets Secret**: Never commit .env files with secrets to version control:

   ```bash
   # .gitignore
   .env
   .env.*
   !.env.example
   ```

8. **Provide .env.example**: Include a template showing all available settings:

   ```bash
   # .env.example
   PROJECT_NAME="My App"
   DEBUG=False
   DATABASE_URL="postgresql+asyncpg://user:pass@localhost/db"
   API_KEY="your-api-key-here"
   ```

## Development vs Production

### Development

```bash
# .env.development
DEBUG=True
DATABASE_URL="postgresql+asyncpg://localhost/dev_db"
REDIS_URL="redis://localhost:6379/0"
LOG_LEVEL="DEBUG"
```

### Production

```bash
# .env.production
DEBUG=False
DATABASE_URL="postgresql+asyncpg://prod-db:5432/app_db"
REDIS_URL="redis://prod-redis:6379/0"
LOG_LEVEL="INFO"
API_KEY="${SECRET_API_KEY}"  # Loaded from secure vault
```

## References

- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Pydantic Validation](https://docs.pydantic.dev/latest/concepts/validators/)
- [Python-dotenv](https://github.com/theskumar/python-dotenv)
