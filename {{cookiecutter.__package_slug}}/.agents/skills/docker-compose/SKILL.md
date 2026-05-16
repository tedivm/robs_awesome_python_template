---
name: docker-compose
description: "Work with the Docker Compose development environment. Use when: starting or stopping services, inspecting logs, opening a shell in a container, resetting the database, or understanding the service topology."
---

# Docker Compose Development Environment

> **context7**: If the `mcp_context7` tool is available, resolve and load the full Docker Compose documentation before modifying `compose.yaml` or using advanced CLI options:
> ```
> mcp_context7_resolve-library-id: "docker compose"
> mcp_context7_get-library-docs: /docker/compose
> ```

The development environment runs entirely through Docker Compose. All services are defined in `compose.yaml`.

---

## Services

{%- if cookiecutter.include_fastapi == "y" %}
| `www`      | FastAPI application server                   |
{%- endif %}
{%- if cookiecutter.include_celery == "y" %}
| `celery-scheduler` | Celery Beat scheduler for periodic tasks |
| `celery-node`  | Celery worker for background tasks         |
{%- endif %}
{%- if cookiecutter.include_quasiqueue == "y" %}
| `qq`         | QuasiQueue multiprocessing runner          |
{%- endif %}
{%- if cookiecutter.include_sqlalchemy == "y" %}
| `db`         | PostgreSQL database                        |
{%- endif %}
{%- if cookiecutter.include_celery == "y" or cookiecutter.include_aiocache == "y" %}
| `redis`      | Redis cache / task broker                  |
{%- endif %}

---

## Essential Commands

### Start / Stop

```bash
# Start all services in the background
docker compose up -d

# Start with live rebuild on file changes
docker compose up --watch

# Stop all services (preserves volumes — data is retained)
docker compose down

# Stop all services AND remove volumes (full reset — destroys all data)
docker compose down --volumes --remove-orphans

# Restart all services without destroying containers or volumes
docker compose restart

# Restart a single service
docker compose restart www
```

### Logs

```bash
# View recent logs from all services
docker compose logs

# Follow (tail) logs from all services in real-time
docker compose logs -f

# Follow logs from a specific service
docker compose logs -f www
```

### Status and Inspection

```bash
# List running services and their status
docker compose ps

# Open a bash shell inside a running service
docker compose exec www bash
```

---

## Common Workflows

### Start a fresh development environment

```bash
docker compose up -d
docker compose logs -f   # watch until all services are healthy
```

### Full reset (wipe all data and restart)

```bash
docker compose down -v
docker compose up -d
```

### Debug a service startup failure

```bash
docker compose logs --tail 50 www
# or follow real-time:
docker compose logs -f www
```

### Run a one-off command inside a service

```bash
# Run in a new container (use for migrations, one-off scripts)
docker compose run --rm www bash

# Execute in an already-running container (use for debugging live services)
docker compose exec www bash
```

---

## Notes

- All Docker-specific files (Dockerfiles, prestart scripts) live in the `docker/` folder.
- The developer `.env` file is loaded automatically by Compose — make sure it's populated before starting.

---

## Further Reading

- [docs/dev/docker.md](../../docs/dev/docker.md) — Full Docker developer guide covering service topology, volume management, hot-reload behavior, and multi-service debugging.
- [Docker Compose Docs](https://docs.docker.com/compose/)
