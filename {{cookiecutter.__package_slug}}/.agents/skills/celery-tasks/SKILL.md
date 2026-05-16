---
name: celery-tasks
description: "Create or modify Celery tasks and periodic task configuration. Use when: adding new background tasks, setting up periodic/scheduled tasks, configuring Celery workers, or understanding the Celery app setup."
---

# Celery Tasks

> **context7**: If the `mcp_context7` tool is available, resolve and load the full `celery` documentation before making any changes to the task system:
> ```
> mcp_context7_resolve-library-id: "celery"
> mcp_context7_get-library-docs: <resolved-id>
> ```

The Celery application is defined in `{{cookiecutter.__package_slug}}/celery.py`. Tasks are exposed via the `@celery.task` decorator.

---

## Defining Tasks

Import the `celery` app instance and decorate functions:

```python
from logging import getLogger
from {{cookiecutter.__package_slug}}.celery import celery

logger = getLogger(__name__)


@celery.task
def send_email(to: str, subject: str, body: str) -> dict[str, str]:
    """Send an email asynchronously."""
    logger.info(f"Sending email to {to}: {subject}")
    return {"status": "sent", "to": to}
```

**Rules:**
- Use `logger` (never `print`) for all output
- Pass IDs, not objects — tasks serialize arguments, complex objects can't be serialized reliably
- Return simple types (dict, list, primitives) — not ORM instances

---

## Task Organization

Organize tasks in separate modules under `{{cookiecutter.__package_slug}}/tasks/`:

```
{{cookiecutter.__package_slug}}/
├── celery.py           # Celery app configuration
└── tasks/
    ├── __init__.py
    ├── email.py        # Email-related tasks
    └── reports.py      # Report generation tasks
```

Import task modules in `{{cookiecutter.__package_slug}}/celery.py` to ensure registration:

```python
from {{cookiecutter.__package_slug}}.tasks import email, reports
```

---

## Calling Tasks

```python
# Fire and forget
send_email.delay("user@example.com", "Welcome", "Thanks for signing up!")

# With options
send_email.apply_async(
    args=["user@example.com", "Welcome", "Body"],
    countdown=60,       # Execute after 60 seconds
    queue='emails',     # Route to specific queue
)

# Get result (blocking)
result = send_email.delay("user@example.com", "Hello", "Body")
output = result.get(timeout=10)
```

---

## Periodic Tasks

Use the `on_after_configure` signal in `{{cookiecutter.__package_slug}}/celery.py` (Celery's documented pattern for periodic task registration):

```python
from celery import Celery
from celery.schedules import crontab

@celery.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs) -> None:
    logger.info("Setting up periodic tasks")
    sender.add_periodic_task(300.0, cleanup_old_data.s(), name="Cleanup every 5 min")
    sender.add_periodic_task(
        crontab(hour=2, minute=0),
        generate_report.s(),
        name="Daily report at 2 AM"
    )
```

> **Note:** Use `on_after_finalize` instead of `on_after_configure` only when periodic tasks reference tasks defined in external modules, to ensure the task registry is fully populated before registration.

---

{%- if cookiecutter.include_sqlalchemy == "y" %}

## Database Access in Tasks

Use the project's `get_session` with an async context manager. Wrap async work in a single `asyncio.run()` call:

```python
import asyncio
from {{cookiecutter.__package_slug}}.services.db import get_session

@celery.task
def process_user_sync(user_id: int) -> dict[str, str]:
    return asyncio.run(process_user(user_id))

async def process_user(user_id: int) -> dict[str, str]:
    async with get_session() as session:
        # ... async DB operations
        pass
    return {"status": "done"}
```

> **Warning:** `asyncio.run()` creates a new event loop. It will raise `RuntimeError` if called from within an existing event loop (e.g., when using Celery's `gevent` or `eventlet` worker pool). In those cases, use `asyncio.get_event_loop().run_until_complete()` or configure Celery with the `asynpool` worker.

---

{%- endif %}

{%- if cookiecutter.include_aiocache == "y" %}

## Cache Integration

Caches are automatically initialized on `on_after_configure`. Use them directly in tasks:

```python
import asyncio
from {{cookiecutter.__package_slug}}.services.cache import get_cached, set_cached

@celery.task
def cached_task(key: str) -> str | None:
    async def _run() -> str | None:
        value = await get_cached(key)
        if value is None:
            value = compute_expensive_value()
            await set_cached(key, value, alias="persistent")
        return value
    return asyncio.run(_run())
```

> **Note:** When calling multiple async functions, batch them in a single `async def` and wrap with one `asyncio.run()` call. Calling `asyncio.run()` multiple times in the same function will raise `RuntimeError`.

---

{%- endif %}

## Retries

```python
from logging import getLogger

logger = getLogger(__name__)

@celery.task(bind=True, max_retries=3, default_retry_delay=60)
def fragile_task(self) -> None:
    try:
        do_risky_thing()
    except Exception as exc:
        logger.exception("Task failed, retrying")
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
```

> **Note:** Always pass the caught exception to `self.retry(exc=exc)` so the original traceback is preserved in logs and raised when `max_retries` is exceeded.

---

## Style Checklist

- [ ] Task uses `logger` (not `print`) for all output
- [ ] Task accepts IDs, not complex objects
- [ ] Task returns simple types (dict, list, primitives)
- [ ] Task module is imported in `{{cookiecutter.__package_slug}}/celery.py` for registration
- [ ] `@celery.task` decorator used (not standalone `@app.task`)
- [ ] Async tasks use a single `asyncio.run()` wrapper (batch multiple awaits in one `async def`)
- [ ] Retries use `bind=True` with `self.retry(exc=exc)`
- [ ] Periodic tasks use `on_after_configure` signal (not `on_after_finalize`)

---

## Further Reading

- [docs/dev/celery.md](../../docs/dev/celery.md) — Full Celery developer guide
- [Celery Docs](https://docs.celeryq.dev/)
