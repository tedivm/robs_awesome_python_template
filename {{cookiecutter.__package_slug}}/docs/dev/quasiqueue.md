# QuasiQueue Integration

This project uses [QuasiQueue](https://github.com/tedivm/quasiqueue), a multiprocessing library for Python that simplifies the creation and management of long-running jobs.

## Overview

QuasiQueue handles all the complexity of multiprocessing so you only need to define two simple functions:

- **Writer**: An async generator that yields items when the queue is low
- **Reader**: A function that processes individual items from the queue

The library handles process creation/cleanup, signal management, cross-process communication, and all the other complexity that makes working with multiprocessing difficult.

## Configuration

### Basic Setup

QuasiQueue is initialized in `{{cookiecutter.__package_slug}}/qq.py` with three main components:

```python
from quasiqueue import QuasiQueue

# 1. Writer: yields items to queue
async def writer(desired: int):
    """Called when queue needs items."""
    for x in range(0, desired):
        yield x

# 2. Reader: processes items from queue
async def reader(identifier: int | str):
    """Processes one item."""
    print(f"Processing: {identifier}")

# 3. Runner: orchestrates everything
runner = QuasiQueue(
    settings.project_name,
    reader=reader,
    writer=writer,
    settings=settings
)
```

### Settings Configuration

Your Settings class inherits from `QuasiQueueSettings` to get QuasiQueue configuration:

```python
from quasiqueue import Settings as QuasiQueueSettings

class Settings(QuasiQueueSettings, ...):
    project_name: str = "my_project"
```

Environment variables use your project name as a prefix:

```bash
# Basic configuration (using TEST_FULL_DOCS as example prefix)
TEST_FULL_DOCS_NUM_PROCESSES=4              # Number of reader processes (default: 2)
TEST_FULL_DOCS_MAX_QUEUE_SIZE=500           # Maximum queue size (default: 300)
TEST_FULL_DOCS_LOOKUP_BLOCK_SIZE=20         # Items writer fetches per call (default: 10)

# Performance tuning
TEST_FULL_DOCS_CONCURRENT_TASKS_PER_PROCESS=4  # Async tasks per process (default: 4)
TEST_FULL_DOCS_MAX_JOBS_PER_PROCESS=200     # Jobs before process restart (default: 200)
TEST_FULL_DOCS_PREVENT_REQUEUING_TIME=300   # Seconds to prevent requeuing (default: 300)

# Sleep intervals
TEST_FULL_DOCS_EMPTY_QUEUE_SLEEP_TIME=1.0   # Sleep when writer returns nothing (default: 1.0)
TEST_FULL_DOCS_FULL_QUEUE_SLEEP_TIME=5.0    # Sleep when queue is full (default: 5.0)
TEST_FULL_DOCS_QUEUE_INTERACTION_TIMEOUT=0.01  # Queue lock timeout (default: 0.01)
TEST_FULL_DOCS_GRACEFUL_SHUTDOWN_TIMEOUT=30 # Graceful shutdown wait (default: 30)
```

All settings have sensible defaults and are optional.

## Writer Function

The writer is an **async generator** that yields items to be processed:

```python
async def writer(desired: int):
    """Yields items when queue is low.

    Args:
        desired: Suggested number of items to yield (optional to honor)
    """
    # Simple range example
    for x in range(0, desired):
        yield x
```

### Writer Behavior

- Called automatically when the queue needs items (below 30% full)
- Receives a `desired` parameter suggesting how many items to yield
- Can honor, ignore, or partially honor the `desired` count
- Should `yield` items that can be pickled (strings, integers, simple objects)
- Can return or yield nothing when no work is available

### Database Example

```python
async def writer(desired: int):
    """Fetch pending jobs from database."""
    async with get_db_session() as session:
        jobs = await session.execute(
            select(Job)
            .where(Job.status == "pending")
            .limit(desired)
        )
        for job in jobs.scalars():
            yield job.id
    # No explicit None needed - generator ends naturally
```

### Writer Features

QuasiQueue automatically:

- Prevents duplicate items from being re-queued within a time window
- Sleeps when writer yields nothing (empty queue sleep time)
- Sleeps when queue is full (full queue sleep time)
- Passes optional `settings` argument if function signature includes it

## Reader Function

The reader processes individual items from the queue:

```python
async def reader(identifier: int | str):
    """Processes one item from queue.

    Args:
        identifier: Item yielded by writer function
    """
    print(f"Processing {identifier}")
```

### Reader Variations

The reader can be sync or async:

```python
# Async reader (preferred for I/O bound work)
async def reader(item: int | str):
    await process_item(item)

# Sync reader (for CPU bound work)
def reader(item: int | str):
    process_item(item)
```

### Reader with Context

Use a context function to share resources across reader calls:

```python
def context():
    """Initialize once per reader process."""
    return {
        'http': get_http_connection_pool(),
        'dbengine': get_db_engine()
    }

async def reader(item: int | str, ctx: dict):
    """ctx contains result from context function."""
    async with ctx['dbengine'].session() as session:
        # Use shared database engine
        job = await session.get(Job, item)
        await job.process()

runner = QuasiQueue(
    settings.project_name,
    reader=reader,
    writer=writer,
    context=context,  # Pass context function
    settings=settings
)
```

### Reader with Settings

Access settings in your reader:

```python
async def reader(item: int | str, settings: dict):
    """settings is dict of all QuasiQueue settings."""
    if settings.get('debug'):
        print(f"Debug: Processing {item}")

    max_retries = settings.get('max_retries', 3)
    # Use settings as needed
```

### Concurrent Tasks

For async readers, `concurrent_tasks_per_process` controls parallelism:

```bash
# Each process runs up to 4 reader tasks concurrently
TEST_FULL_DOCS_CONCURRENT_TASKS_PER_PROCESS=4
```

If you have 4 processes with 4 concurrent tasks each, that's 16 reader instances running simultaneously.

## Running QuasiQueue

### Command Line

Run as a standalone process:

```bash
# Run the qq module directly
python -m {{cookiecutter.__package_slug}}.qq
```

### In Code

```python
import asyncio
from {{cookiecutter.__package_slug}}.qq import runner

if __name__ == "__main__":
    asyncio.run(runner.main())
```

### What Happens

When you run QuasiQueue:

1. Creates a multiprocess queue
2. Launches reader processes (number controlled by `num_processes`)
3. Writer fills the queue with items
4. Reader processes pull items and process them
5. Processes are restarted after `max_jobs_per_process` jobs
6. Handles SIGTERM/SIGINT for graceful shutdown
{%- if cookiecutter.include_aiocache == "y" %}

## Cache Integration

If using aiocache, caches are automatically initialized before the QuasiQueue runner starts and are available in your reader functions:

```python
from {{cookiecutter.__package_slug}}.services.cache import cache

async def reader(item: int | str):
    """Reader can access initialized caches."""
    # Check cache first
    cached_result = await cache.get(f'result_{item}')
    if cached_result:
        return cached_result

    # Process and cache result
    result = await process_item(item)
    await cache.set(f'result_{item}', result, ttl=3600)
    return result
```

Cache initialization is handled automatically by the application startup, so you don't need to worry about it in your QuasiQueue functions.
{%- endif %}

## Testing

### Component Tests

Test writer and reader functions individually:

```python
"""Tests for QuasiQueue components."""
import pytest
from {{cookiecutter.__package_slug}}.qq import runner, writer, reader


def test_runner_exists():
    """QuasiQueue runner should be instantiated."""
    assert runner is not None


def test_runner_has_settings():
    """Runner should have settings configured."""
    assert hasattr(runner, "settings")
    assert runner.settings is not None


def test_writer_is_async_generator():
    """Writer should be an async generator function."""
    import inspect
    assert inspect.isasyncgenfunction(writer)


@pytest.mark.asyncio
async def test_writer_yields_items():
    """Writer should yield expected number of items."""
    desired = 5
    results = []

    async for item in writer(desired):
        results.append(item)

    assert len(results) == desired
    assert results == list(range(0, desired))


@pytest.mark.asyncio
async def test_reader_processes_item():
    """Reader should process an item without error."""
    # Should not raise exceptions
    await reader(42)
```

### Context Function Tests

If using a context function:

```python
import inspect
from {{cookiecutter.__package_slug}}.qq import context, reader


def test_context_returns_dict():
    """Context should return a dictionary of resources."""
    if context:
        ctx = context()
        assert isinstance(ctx, dict)


@pytest.mark.asyncio
async def test_reader_uses_context():
    """Reader should work with context resources."""
    if context:
        ctx = context() if not inspect.iscoroutinefunction(context) else await context()

        # Check if reader accepts ctx parameter
        sig = inspect.signature(reader)
        if 'ctx' in sig.parameters:
            await reader(1, ctx=ctx)
```

### Integration Tests

For full workflow testing:

```python
@pytest.mark.asyncio
async def test_quasiqueue_workflow():
    """Test complete QuasiQueue workflow."""
    from quasiqueue import QuasiQueue, Settings

    processed = []

    async def test_writer(desired: int):
        for x in range(0, 10):
            yield x

    async def test_reader(item: int):
        processed.append(item)

    test_runner = QuasiQueue(
        "test_queue",
        reader=test_reader,
        writer=test_writer,
        settings=Settings(
            num_processes=2,
            max_queue_size=50,
            graceful_shutdown_timeout=1
        )
    )

    # Run briefly then cancel
    import asyncio
    task = asyncio.create_task(test_runner.main())
    await asyncio.sleep(2)
    task.cancel()

    # Should have processed some items
    assert len(processed) >= 5
```

## Best Practices

### Process Configuration

**Number of Processes**: Match to workload type

- CPU-bound work: Match CPU core count
- I/O-bound work: Can exceed core count (2-4x)

```bash
# CPU-bound: intensive calculations
TEST_FULL_DOCS_NUM_PROCESSES=8  # Match your CPU cores

# I/O-bound: database queries, HTTP requests
TEST_FULL_DOCS_NUM_PROCESSES=16  # Can exceed cores
TEST_FULL_DOCS_CONCURRENT_TASKS_PER_PROCESS=4  # Even more parallelism
```

**Process Recycling**: Prevent memory leaks by restarting processes

```bash
# Restart reader process after 200 jobs
TEST_FULL_DOCS_MAX_JOBS_PER_PROCESS=200
```

### Writer Optimization

**Honor `desired` Parameter**: Better performance when you yield close to requested count

```python
async def writer(desired: int):
    # Good: respects desired count
    jobs = await fetch_pending_jobs(limit=desired)
    for job in jobs:
        yield job.id
```

**Batch Database Queries**: Fetch multiple items at once

```python
async def writer(desired: int):
    # Efficient: single query for multiple items
    async with get_db_session() as session:
        jobs = await session.execute(
            select(Job)
            .where(Job.status == "pending")
            .limit(desired)
        )
        for job in jobs.scalars():
            yield job.id
```

**Signal Empty Queue**: Return/yield nothing when no work available

```python
async def writer(desired: int):
    jobs = await fetch_pending_jobs(limit=desired)

    if not jobs:
        # QuasiQueue will sleep (empty_queue_sleep_time)
        return

    for job in jobs:
        yield job.id
```

### Reader Optimization

**Prefer Async Readers**: Better for I/O-bound work

```python
# Good: async reader with concurrent tasks
async def reader(item: int, ctx: dict):
    async with ctx['http'].get(url) as response:
        data = await response.json()
        # Process data
```

**Use Context Function**: Share expensive resources

```python
def context():
    """Initialize once per process, not per job."""
    return {
        'http': get_http_connection_pool(),
        'db': get_db_engine(),
        'redis': get_redis_pool()
    }

async def reader(item: int, ctx: dict):
    # Reuse pooled connections
    async with ctx['db'].session() as session:
        # Database work
        pass
```

**Error Handling**: Prevent process crashes

```python
async def reader(item: int):
    try:
        # Process item
        await process(item)
    except Exception as e:
        logger.error(f"Failed to process {item}: {e}")
        # Don't let exception kill the process
```

### Shutdown Handling

QuasiQueue automatically handles graceful shutdown:

- **SIGTERM**: Waits for readers to finish (up to `graceful_shutdown_timeout`)
- **SIGINT**: Same as SIGTERM
- **After Timeout**: Forcefully terminates remaining processes

```bash
# Give readers 60 seconds to finish current work
TEST_FULL_DOCS_GRACEFUL_SHUTDOWN_TIMEOUT=60
```

For quick shutdown during development:

```bash
# Shorter timeout for faster restart cycles
TEST_FULL_DOCS_GRACEFUL_SHUTDOWN_TIMEOUT=5
```

## Development vs Production

### Development

Focus on debuggability:

```bash
# .env.development
TEST_FULL_DOCS_NUM_PROCESSES=1              # Single process easier to debug
TEST_FULL_DOCS_MAX_QUEUE_SIZE=20            # Smaller queue
TEST_FULL_DOCS_DEBUG=true                   # Enable debug logging
TEST_FULL_DOCS_GRACEFUL_SHUTDOWN_TIMEOUT=2  # Fast shutdown for restarts
```

Add logging for visibility:

```python
import logging

logger = logging.getLogger(__name__)

async def reader(identifier: int | str):
    logger.info(f"Started processing {identifier}")
    # Process item
    logger.info(f"Completed {identifier}")
```

### Production

Optimize for throughput and reliability:

```bash
# .env.production
TEST_FULL_DOCS_NUM_PROCESSES=16             # Scale to workload
TEST_FULL_DOCS_MAX_QUEUE_SIZE=500           # Larger buffer
TEST_FULL_DOCS_CONCURRENT_TASKS_PER_PROCESS=4  # More parallelism
TEST_FULL_DOCS_MAX_JOBS_PER_PROCESS=200     # Memory leak protection
TEST_FULL_DOCS_GRACEFUL_SHUTDOWN_TIMEOUT=60 # Don't lose work
```

Monitor with metrics:

```python
from prometheus_client import Counter, Histogram

jobs_processed = Counter('jobs_processed_total', 'Total jobs processed')
job_duration = Histogram('job_duration_seconds', 'Job processing time')

async def reader(item: int | str):
    with job_duration.time():
        # Process item
        pass
    jobs_processed.inc()
```

### Deployment

**Daemonization**: Run as a service

```ini
# systemd unit file
[Service]
ExecStart=/path/to/venv/bin/python -m {{cookiecutter.__package_slug}}.qq
Restart=always
```

**Docker**: Run in a container

```dockerfile
CMD ["python", "-m", "{{cookiecutter.__package_slug}}.qq"]
```

**Health Monitoring**: Track queue metrics

- Queue depth (items waiting)
- Processing rate (items/second)
- Process count (should match config)
- Error rate

**Graceful Deploys**: Use SIGTERM for zero-downtime

```bash
# Send SIGTERM, processes finish current work then exit
kill -TERM <pid>
```

## Additional Resources

- [QuasiQueue GitHub Repository](https://github.com/tedivm/quasiqueue)
- [QuasiQueue README Documentation](https://github.com/tedivm/quasiqueue/blob/main/README.md) - Includes additional use case examples for web servers, web scraping, image processing, and more
- [Python Multiprocessing Documentation](https://docs.python.org/3/library/multiprocessing.html)
