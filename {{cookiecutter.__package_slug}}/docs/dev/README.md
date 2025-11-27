# Developer Documentation

Welcome to the developer documentation! This directory contains comprehensive guides for working with this project's features, tools, and workflows.

## Getting Started

New to this project? Start here:

1. **[Makefile](./makefile.md)** - Essential commands for development, testing, and building
2. **[Dependencies](./dependencies.md)** - Managing project dependencies, virtual environments, and package installation
3. **[Settings](./settings.md)** - Environment configuration and settings management
{%- if cookiecutter.include_docker == "y" %}
4. **[Docker](./docker.md)** - Containerization, deployment, and local development with Docker
{%- endif %}

## Core Features

{%- if cookiecutter.include_sqlalchemy == "y" %}

### [Database](./database.md)

SQLAlchemy ORM integration, models, migrations with Alembic, and database patterns.
{%- endif %}
{%- if cookiecutter.include_aiocache == "y" %}

### [Caching](./cache.md)

Redis-backed caching with aiocache for performance optimization.
{%- endif %}
{%- if cookiecutter.include_fastapi == "y" %}

### [REST API](./api.md)

FastAPI web framework, endpoints, middleware, and API development.
{%- endif %}
{%- if cookiecutter.include_cli == "y" %}

### [CLI](./cli.md)

Command-line interface built with Typer for management and automation tasks.
{%- endif %}
{%- if cookiecutter.include_celery == "y" %}

### [Celery](./celery.md)

Distributed task queue for background processing and asynchronous jobs.
{%- endif %}
{%- if cookiecutter.include_quasiqueue == "y" %}

### [QuasiQueue](./quasiqueue.md)

Lightweight message queue for simpler asynchronous task handling.
{%- endif %}
{%- if cookiecutter.include_jinja2 == "y" %}

### [Templates](./templates.md)

Jinja2 templating for HTML rendering and template-based content generation.
{%- endif %}

## Development Practices

### [Testing](./testing.md)

Comprehensive testing guide covering pytest, fixtures, async testing, mocking, and code coverage.

### [Documentation](./documentation.md)

Standards and best practices for writing and maintaining project documentation.
{%- if cookiecutter.include_github_actions == "y" %}

### [GitHub Actions](./github.md)

CI/CD workflows for testing, linting, building, and deployment automation.
{%- endif %}
{%- if cookiecutter.publish_to_pypi == "y" %}

### [PyPI](./pypi.md)

Publishing packages to the Python Package Index.
{%- endif %}

## Project-Specific Documentation

As your project grows, add documentation for:

- **Architecture** - System design, component interactions, and architectural decisions
- **API Reference** - Detailed API endpoints, request/response formats, and authentication
- **Deployment** - Production deployment procedures, monitoring, and operations
- **Troubleshooting** - Common issues, debugging techniques, and solutions
- **Contributing** - Guidelines for contributors and development workflows

## Documentation Standards

All documentation in this project follows the standards outlined in [documentation.md](./documentation.md). When adding new documentation:

- Use real, working code examples from this project
- Include practical usage patterns
- Test all code examples before publishing
- Keep documentation updated as code changes
- Follow the established structure and style

## Quick Reference

- **Setup**: Run `make install` to set up your development environment
- **Testing**: Run `make tests` for full test suite, see [testing.md](./testing.md) for details
- **Formatting**: Run `make chores` before committing to fix formatting issues
- **Configuration**: See [settings.md](./settings.md) for environment variables and settings
{%- if cookiecutter.include_docker == "y" %}
- **Local Development**: Use `docker compose up` for local services, see [docker.md](./docker.md)
{%- endif %}
- **All Make Commands**: See [makefile.md](./makefile.md) for complete reference

---

*This documentation is maintained by the development team. If you find issues or have suggestions, please contribute improvements!*
