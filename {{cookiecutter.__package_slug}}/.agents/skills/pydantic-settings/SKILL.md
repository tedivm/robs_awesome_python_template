---
name: pydantic-settings
description: "Add or modify application configuration settings. Use when: adding new environment variables, settings fields, understanding settings conventions, working with secrets, or configuring optional vs required settings."
---

# Pydantic Settings

> **context7**: If the `context7` tools are available, resolve and load the full `pydantic-settings` documentation before adding or modifying any settings:
> ```
> context7_resolve-library-id: "pydantic-settings"
> context7_query-docs: <resolved-id> "your query"
> ```

All application configuration is managed through the `pydantic-settings` library. Settings are defined in a single class and loaded from the environment and `.env` file.

---

## Key Rules

- **One settings class**: The main `Settings` class lives at `{{cookiecutter.__package_slug}}/conf/settings.py`. Always update this existing class — never create a new settings class.
- **Secrets use `SecretStr` or `SecretBytes`**: Any value that is sensitive (passwords, tokens, API keys) must be wrapped in one of these types.
- **Optional settings default to `None`**: Never use empty strings as a sentinel for "not set".
- **All fields use `Field()`**: Include a `description=` for every field so operators know what it does.

---

## Pattern

```python
# {{cookiecutter.__package_slug}}/conf/settings.py
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Regular setting with a default
    project_name: str = Field(default="{{ cookiecutter.__package_slug }}", description="Human-readable project name")

    # Optional sensitive setting — defaults to None, not empty string
    api_key: SecretStr | None = Field(
        default=None,
        description="API key for external service. Leave unset to disable.",
    )

    # Optional non-sensitive setting
    max_connections: int = Field(
        default=10,
        description="Maximum number of connections",
    )
```

---

## Accessing Secrets

`SecretStr` wraps the value to prevent accidental logging. Access the actual value explicitly when needed:

```python
settings.api_key.get_secret_value() if settings.api_key else None
```

---

## Optional vs Required Fields

| Pattern                         | Behavior                                              |
| ------------------------------- | ----------------------------------------------------- |
| `field: str = Field(...)`       | Required — raises `ValidationError` if not set       |
| `field: str = Field(default=x)` | Optional with default                                 |
| `field: str \| None = Field(default=None)` | Optional, absent means `None`          |

Never use `""` as a default for "not configured":

```python
# Bad
smtp_host: str = Field(default="")

# Good
smtp_host: str | None = Field(default=None, description="SMTP server hostname. None disables email.")
```

---

## Environment Variable Naming

`pydantic-settings` maps field names to environment variable names automatically using the field name in uppercase:

```
project_name  →  PROJECT_NAME
database_url  →  DATABASE_URL
```

---

## Adding a New Setting

1. Open `{{cookiecutter.__package_slug}}/conf/settings.py`.
2. Add the field to the existing `Settings` class with `Field(description=...)`.
3. Use `SecretStr` if the value is sensitive.
4. Default to `None` (not `""`) if the setting is optional.
5. Update `.env.example` with the new variable name and a placeholder value or explanation.

---

## Developer Environment

- Settings are loaded from `.env` in the project root (gitignored).
- `.env.example` is the template for new developers — keep it updated with every new setting.

---

## Further Reading

- [docs/dev/settings.md](../../docs/dev/settings.md) — Full settings developer guide covering all configuration modules, accessing settings in different component types, and environment variable conventions.
- [Pydantic Settings Docs](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
