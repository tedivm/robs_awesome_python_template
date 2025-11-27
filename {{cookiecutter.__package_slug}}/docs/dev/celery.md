# Celery

This project uses [Celery](https://docs.celeryq.dev/), a distributed task queue system for processing asynchronous and scheduled tasks in Python.

## Configuration

The Celery application is defined in `{{cookiecutter.__package_slug}}/celery.py`. Unlike other components, Celery does NOT read configuration from the project's Settings class. Instead, Celery must be configured using environment variables.

### Required Environment Variable

- **CELERY_BROKER_URL**: Message broker URL (required)
  - Redis example: `redis://localhost:6379/0`
  - RabbitMQ example: `amqp://guest:guest@localhost:5672//`

Set this environment variable before running Celery workers:

```bash
export CELERY_BROKER_URL="redis://localhost:6379/0"
```

### Optional Configuration

Celery can be further configured using additional environment variables prefixed with `CELERY_` or by creating a `celeryconfig.py` file in your project root. See the [Celery Configuration Documentation](https://docs.celeryq.dev/en/stable/userguide/configuration.html) for all available options.

## Defining Tasks

### Basic Task

Create tasks by decorating functions with `@celery.task`:

```python
from {{cookiecutter.__package_slug}}.celery import celery

@celery.task
def send_email(to: str, subject: str, body: str):
    """Send an email asynchronously."""
    # Email sending logic here
    print(f"Sending email to {to}: {subject}")
    return {"status": "sent", "to": to}
```

### Task with Options

Configure task behavior with decorator options:

```python
@celery.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,),
    retry_backoff=True,
)
def process_payment(self, payment_id: int):
    """Process a payment with automatic retries."""
    try:
        # Payment processing logic
        return {"payment_id": payment_id, "status": "processed"}
    except PaymentError as exc:
        # Manual retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
```

{%- if cookiecutter.include_sqlalchemy == "y" %}

### Async Task (with Database Access)

Use async tasks for I/O-bound operations:

```python
from {{cookiecutter.__package_slug}}.services.db import get_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

@celery.task
def process_user_sync(user_id: int):
    """Synchronous wrapper for async task."""
    import asyncio
    return asyncio.run(process_user(user_id))

async def process_user(user_id: int):
    """Process user data with async database access."""
    engine = await get_engine()
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession)

    async with SessionLocal() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if user:
            # Process user
            user.last_processed = datetime.now()
            await session.commit()

        return {"user_id": user_id, "processed": bool(user)}
```

{%- endif %}

## Calling Tasks

### Fire and Forget

Execute a task asynchronously without waiting for results:

```python
# Call the task
send_email.delay("user@example.com", "Welcome", "Thanks for signing up!")

# Or with apply_async for more options
send_email.apply_async(
    args=["user@example.com", "Welcome", "Thanks for signing up!"],
    countdown=60,  # Execute after 60 seconds
)
```

### Getting Results

Retrieve task results synchronously:

```python
# Call task and get AsyncResult object
result = send_email.delay("user@example.com", "Hello", "Message body")

# Wait for result (blocking)
output = result.get(timeout=10)  # Raises TimeoutError if not done in 10s
print(output)  # {"status": "sent", "to": "user@example.com"}

# Check task state
print(result.state)  # 'PENDING', 'STARTED', 'SUCCESS', 'FAILURE', etc.
```

### Task Options

Use `apply_async` for advanced options:

```python
send_email.apply_async(
    args=["user@example.com", "Subject", "Body"],
    countdown=300,        # Delay 5 minutes
    expires=3600,         # Expire after 1 hour
    priority=9,           # Higher priority (0-9)
    queue='emails',       # Route to specific queue
    retry=True,           # Enable retries
    retry_policy={
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.2,
    }
)
```

## Periodic Tasks (Celery Beat)

### Configuration

Periodic tasks can be configured in two ways:

**Method 1: Using signal handler** (template default):

```python
@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    """Configure periodic tasks when Celery is ready."""
    # Add a task that runs every 15 seconds
    sender.add_periodic_task(15.0, hello_world.s(), name="Test Task")

    # Add a task with crontab schedule
    from celery.schedules import crontab
    sender.add_periodic_task(
        crontab(hour=2, minute=0),
        cleanup_old_data.s(),
        name='Daily Cleanup'
    )
```

**Method 2: Using beat_schedule** (alternative):

```python
from celery.schedules import crontab

celery.conf.beat_schedule = {
    'cleanup-old-data': {
        'task': '{{cookiecutter.__package_slug}}.tasks.cleanup_old_data',
        'schedule': crontab(hour=2, minute=0),  # Run daily at 2 AM
    },
    'send-weekly-report': {
        'task': '{{cookiecutter.__package_slug}}.tasks.send_weekly_report',
        'schedule': crontab(day_of_week='monday', hour=9, minute=0),
    },
    'check-status-every-5-min': {
        'task': '{{cookiecutter.__package_slug}}.tasks.check_status',
        'schedule': 300.0,  # Run every 5 minutes (in seconds)
    },
}
```

### Schedule Types

**Crontab Schedule** (like Unix cron):

```python
from celery.schedules import crontab

# Every midnight
crontab(hour=0, minute=0)

# Every Monday at 9 AM
crontab(day_of_week='monday', hour=9, minute=0)

# Every 15 minutes
crontab(minute='*/15')

# First day of every month
crontab(day_of_month='1', hour=0, minute=0)
```

**Interval Schedule**:

```python
from celery.schedules import schedule

# Every 30 seconds
schedule(run_every=30.0)

# Can also use timedelta
from datetime import timedelta
schedule(run_every=timedelta(hours=1))
```

## Task Organization

Organize tasks in separate modules:

```
{{cookiecutter.__package_slug}}/
├── celery.py           # Celery app configuration
└── tasks/
    ├── __init__.py
    ├── email.py        # Email-related tasks
    ├── reports.py      # Report generation tasks
    └── cleanup.py      # Maintenance tasks
```

Import tasks in `celery.py` to ensure they're registered:

```python
# In {{cookiecutter.__package_slug}}/celery.py
from {{cookiecutter.__package_slug}}.tasks import email, reports, cleanup
```

## Running Workers

### Development

Start a Celery worker in development mode:

```bash
# Basic worker
celery -A {{cookiecutter.__package_slug}}.celery worker --loglevel=info

# With concurrency limit
celery -A {{cookiecutter.__package_slug}}.celery worker --loglevel=info --concurrency=4

# With specific queues
celery -A {{cookiecutter.__package_slug}}.celery worker --loglevel=info -Q celery,emails
```

### Celery Beat (Scheduler)

Run the beat scheduler for periodic tasks:

```bash
# In a separate terminal
celery -A {{cookiecutter.__package_slug}}.celery beat --loglevel=info

# Or combine worker and beat (NOT recommended for production)
celery -A {{cookiecutter.__package_slug}}.celery worker --beat --loglevel=info
```

### Production

Use multiple workers with proper concurrency:

```bash
# Prefork pool (default) - good for CPU-bound tasks
celery -A {{cookiecutter.__package_slug}}.celery worker \
    --loglevel=info \
    --concurrency=8 \
    --pool=prefork

# Eventlet pool - better for I/O-bound tasks
celery -A {{cookiecutter.__package_slug}}.celery worker \
    --loglevel=info \
    --concurrency=100 \
    --pool=eventlet

# Gevent pool - alternative for I/O-bound tasks
celery -A {{cookiecutter.__package_slug}}.celery worker \
    --loglevel=info \
    --concurrency=100 \
    --pool=gevent
```

{%- if cookiecutter.include_docker == "y" %}

### Docker

If Docker is configured:

```bash
# Start worker
docker-compose up celery

# Start beat scheduler
docker-compose up beat
```

{%- endif %}

## Monitoring

### Command Line

Monitor tasks from the command line:

```bash
# List active tasks
celery -A {{cookiecutter.__package_slug}}.celery inspect active

# List scheduled tasks (ETA tasks)
celery -A {{cookiecutter.__package_slug}}.celery inspect scheduled

# List registered tasks
celery -A {{cookiecutter.__package_slug}}.celery inspect registered

# Worker statistics
celery -A {{cookiecutter.__package_slug}}.celery inspect stats

# Ping workers
celery -A {{cookiecutter.__package_slug}}.celery inspect ping
```

{%- if cookiecutter.include_aiocache == "y" %}

## Cache Integration

If aiocache is enabled, the cache setup handler runs automatically:

```python
from {{cookiecutter.__package_slug}}.celery import celery

@celery.task
def task_using_cache():
    """Task that uses caching."""
    from {{cookiecutter.__package_slug}}.services.cache import cache

    # Use cache in tasks
    cache.set("key", "value", ttl=300)
    return cache.get("key")
```

{%- endif %}

## Testing Celery Tasks

### Testing Task Registration

Test that tasks are properly registered with Celery:

```python
# tests/test_celery.py
from {{cookiecutter.__package_slug}}.celery import celery, hello_world


def test_celery_app_exists():
    """Test that Celery app is properly instantiated."""
    assert celery is not None
    assert hasattr(celery, "tasks")


def test_celery_app_name():
    """Test that Celery app has correct name."""
    assert celery.main == "{{cookiecutter.__package_slug}}"


def test_hello_world_task_registered():
    """Test that hello_world task is registered with Celery."""
    assert "{{cookiecutter.__package_slug}}.celery.hello_world" in celery.tasks


def test_hello_world_is_task():
    """Test that hello_world is a Celery task."""
    assert hasattr(hello_world, "delay")
    assert hasattr(hello_world, "apply_async")
    assert callable(hello_world)
```

### Testing Task Execution

Test tasks by calling them directly (synchronously):

```python
def test_hello_world_execution(capsys):
    """Test that hello_world task executes without error."""
    # Run the task directly (not async)
    hello_world()

    # Check that it printed the expected message
    captured = capsys.readouterr()
    assert "Hello World!" in captured.out


def test_task_with_return_value():
    """Test task that returns a value."""
    @celery.task
    def add_numbers(a: int, b: int) -> int:
        return a + b

    # Call directly for testing
    result = add_numbers(2, 3)
    assert result == 5


def test_task_with_args():
    """Test task with multiple arguments."""
    result = process_data(user_id=123, action="update")
    assert result["status"] == "success"
    assert result["user_id"] == 123
```

### Testing Periodic Tasks

Test that periodic tasks are properly configured:

```python
def test_periodic_task_setup_exists():
    """Test that periodic task setup function exists."""
    assert hasattr(celery, "on_after_finalize")


def test_periodic_tasks_registered():
    """Test that periodic tasks are configured."""
    # Note: This requires Celery to be fully configured
    # You may need to call setup_periodic_tasks manually in tests
    from {{cookiecutter.__package_slug}}.celery import setup_periodic_tasks

    # Mock sender
    class MockSender:
        def __init__(self):
            self.periodic_tasks = []

        def add_periodic_task(self, interval, task, name=None):
            self.periodic_tasks.append({
                "interval": interval,
                "task": task,
                "name": name
            })

    sender = MockSender()
    setup_periodic_tasks(sender)

    # Verify periodic task was added
    assert len(sender.periodic_tasks) > 0
    assert sender.periodic_tasks[0]["name"] == "Test Task"
```

### Testing Signal Handlers

Test Celery signal handlers like cache setup:

```python
def test_cache_setup_handler_exists():
    """Test that cache setup signal handler is registered."""
    from {{cookiecutter.__package_slug}}.celery import setup_caches
    assert callable(setup_caches)


def test_cache_setup_imports():
    """Test that cache setup can import required modules."""
    from {{cookiecutter.__package_slug}}.services.cache import configure_caches
    from {{cookiecutter.__package_slug}}.settings import settings

    # Should not raise ImportError
    assert callable(configure_caches)
    assert settings is not None
```

### Testing Task Errors

Test error handling and retries:

```python
def test_task_with_error_handling():
    """Test that task handles errors gracefully."""
    @celery.task(bind=True, max_retries=3)
    def failing_task(self):
        try:
            raise ValueError("Test error")
        except ValueError as exc:
            raise self.retry(exc=exc, countdown=1)

    # Test that task raises retry exception
    with pytest.raises(Exception):
        failing_task()


def test_task_retry_logic():
    """Test task retry configuration."""
    @celery.task(max_retries=3, default_retry_delay=60)
    def retryable_task():
        pass

    assert retryable_task.max_retries == 3
    assert retryable_task.default_retry_delay == 60
```

### Testing with Mocks

Mock external dependencies in task tests:

```python
from unittest.mock import patch, MagicMock


def test_task_with_external_api(monkeypatch):
    """Test task that calls external API."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "success"}

    with patch('requests.get', return_value=mock_response):
        result = fetch_external_data("https://api.example.com")
        assert result["status"] == "success"


def test_task_with_database(monkeypatch):
    """Test task that uses database."""
    # Mock database operations
    mock_session = MagicMock()

    with patch('{{cookiecutter.__package_slug}}.services.db.get_session', return_value=mock_session):
        result = process_user_task(user_id=123)
        assert result is not None
```

## Best Practices

1. **Keep Tasks Small**: Break large operations into smaller, composable tasks that can be chained or grouped

2. **Set Task Timeouts**: Always set time limits to prevent tasks from running indefinitely:

   ```python
   @celery.task(time_limit=300, soft_time_limit=270)
   def long_running_task():
       # Will be terminated after 5 minutes
       pass
   ```

3. **Handle Failures Gracefully**: Use retries and error handling:

   ```python
   @celery.task(bind=True, max_retries=3)
   def fragile_task(self):
       try:
           # Potentially failing operation
           pass
       except Exception as exc:
           raise self.retry(exc=exc, countdown=60)
   ```

4. **Use Task Queues**: Route different task types to different queues:

   ```python
   @celery.task(queue='high-priority')
   def urgent_task():
       pass

   @celery.task(queue='low-priority')
   def background_cleanup():
       pass
   ```

5. **Idempotent Tasks**: Design tasks to be safely retried without side effects - check if work is already done before proceeding

6. **Avoid Passing Complex Objects**: Pass IDs instead of full objects to tasks:

   ```python
   # Good
   @celery.task
   def process_user(user_id: int):
       user = User.query.get(user_id)
       # Process user

   # Bad - objects can't be serialized reliably
   @celery.task
   def process_user(user: User):
       pass
   ```

7. **Monitor Task Performance**: Use Flower or logging to track task execution times and failure rates

## Development vs Production

### Development

```bash
# Single worker with auto-reload
export CELERY_BROKER_URL="redis://localhost:6379/0"
celery -A {{cookiecutter.__package_slug}}.celery worker --loglevel=debug --pool=solo
```

### Production

```bash
# Multiple workers with production settings
export CELERY_BROKER_URL="redis://prod-redis:6379/0"
export CELERY_RESULT_BACKEND="redis://prod-redis:6379/1"

# Worker with proper pool
celery -A {{cookiecutter.__package_slug}}.celery worker \
    --loglevel=info \
    --concurrency=10 \
    --max-tasks-per-child=1000 \
    --time-limit=3600 \
    --soft-time-limit=3300

# Beat scheduler (separate process)
celery -A {{cookiecutter.__package_slug}}.celery beat --loglevel=info
```

## References

- [Celery Documentation](https://docs.celeryq.dev/)
- [Celery Best Practices](https://docs.celeryq.dev/en/stable/userguide/tasks.html#tips-and-best-practices)
- [Redis Documentation](https://redis.io/docs/)
- [Flower Documentation](https://flower.readthedocs.io/)

This project uses [Celery](https://docs.celeryq.dev/en/stable/) and [Celery Beat](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html).
