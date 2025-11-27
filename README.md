# Rob's Awesome Python Template

**The most comprehensive Python project template that scales from simple libraries to enterprise applications**

Transform any Python idea into a production-ready project in minutes. This CookieCutter template provides everything you need to build, test, deploy, and maintain modern Python applications with industry best practices baked in.

## Why Choose This Template?

- **Modern Development Tools**: Get a fully configured environment with Ruff (formatting/linting), mypy (type checking), pytest (testing), and pre-commit hooks ready to use
- **Production-Ready Frameworks**: Optional integration with FastAPI (web APIs), Celery (distributed tasks), SQLAlchemy + Alembic (database ORM), and QuasiQueue (multiprocessing)
- **Professional Infrastructure**: Includes Docker containerization, GitHub Actions CI/CD, Pydantic Settings for configuration, and Makefile automation
- **Developer-Friendly CLI**: Optional Typer integration for building beautiful command-line interfaces with automatic help and shell completion
- **AI Ready**: Pre-configured AGENTS.md file following the open standard compatible with Cursor, Aider, GitHub Copilot, and other AI coding assistants
- **Incredibly Flexible**: Mix and match features to create exactly what you need, from simple libraries to full web applications with automatic cleanup of unused code
- **Modern Python Standards**: Python 3.10+ with async/await support, type hints, contemporary best practices, and pyproject.toml configuration

## Quick Start

```bash
# Install cookiecutter if you haven't already
pip install cookiecutter

# Create your project
cookiecutter gh:tedivm/robs_awesome_python_template
```

Answer a few questions about your project, and you'll have a complete Python application with everything configured and ready to go!

## Core Features (Always Included)

Every project created with this template includes these essential components:

### Development Tools

- **[Makefile](https://www.gnu.org/software/make/manual/html_node/Introduction.html) automation**: Powerful task automation covering setup, testing, formatting, linting, and deployment with simple commands like `make install`, `make test`, and `make publish`
- **Modern pyproject.toml**: Centralized project configuration using the modern Python standard, eliminating legacy setup.py files and consolidating all metadata, dependencies, and tool settings in one place
- **Virtual environment management**: Seamless virtual environment creation and activation with automatic [pyenv](https://github.com/pyenv/pyenv) integration for managing Python versions across development teams
- **[Pre-commit](https://pre-commit.com/) hooks**: Automated code quality checks that run before every commit, catching formatting issues, security vulnerabilities, and common mistakes before they enter your repository

### Code Quality

- **[Ruff](https://docs.astral.sh/ruff/)**: Blazingly fast Python linter and formatter (10-100x faster than Black) that replaces multiple tools (Flake8, isort, Black) with a single, zero-configuration solution written in Rust
- **[mypy](https://mypy.readthedocs.io/en/stable/)**: Industry-standard static type checker that catches type-related bugs before runtime, providing IDE autocompletion and making refactoring safer
- **[pytest](https://docs.pytest.org/)**: Python's most popular testing framework with powerful fixtures, parametrization, full async/await support, and extensive plugin ecosystem for testing web apps, databases, and more
- **Coverage reporting**: Comprehensive test coverage tracking with support for multiprocess and distributed applications, ensuring your tests exercise all code paths

### Configuration & Settings

- **[Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)**: Type-safe configuration management using Pydantic v2, automatically loading and validating settings from environment variables, .env files, and secrets with full IDE support
- **Environment-based config**: Seamless configuration switching between development, staging, and production environments using environment variables with sensible defaults
- **Automatic validation**: Runtime validation with clear error messages for misconfigured values, preventing deployment of broken configurations and catching issues during development

### Publishing & Distribution

- **[setuptools-scm](https://pypi.org/project/setuptools-scm/)**: Automatic semantic versioning derived from git tags and commit history, eliminating manual version updates and ensuring version consistency across your project
- **PyPI publishing**: Streamlined package publishing to PyPI with a single command, including automatic wheel building, source distribution creation, and metadata validation
- **Multi-architecture support**: Cross-platform compatibility for AMD64 and ARM64 architectures, ensuring your applications work natively on Intel/AMD processors, Apple Silicon, and ARM servers

## Optional Integrations

Pick and choose the features you need. Unused components are completely removed from your project.

### Web Applications

**[FastAPI](https://fastapi.tiangolo.com/) Integration**

- Modern, high-performance web framework built on Starlette and Pydantic, providing automatic data validation and serialization
- Automatic interactive API documentation with both Swagger UI and ReDoc interfaces, generated directly from your Python type hints without additional configuration
- Full async/await support for handling thousands of concurrent connections efficiently, perfect for I/O-bound operations like database queries and external API calls
- Static file serving with optimized caching headers for serving frontend applications, images, and assets directly from your API

### Task Processing

**[Celery](https://docs.celeryq.dev/en/stable/) Integration**

- Enterprise-grade distributed task queue for processing millions of tasks per day, with support for task prioritization, routing, and complex workflows using chains, groups, and chords
- Production-proven [Redis](https://redis.io/) broker configuration with connection pooling, automatic retries, and result backend for storing task outcomes and enabling result retrieval
- Pre-configured worker and scheduler (beat) containers for running periodic tasks like cron jobs, with separate deployments for different task types and priorities
- Automatic task retry mechanisms with exponential backoff, task revocation, rate limiting, and comprehensive error handling for building resilient asynchronous systems

**[QuasiQueue](https://github.com/tedivm/quasiqueue) Integration**

- Lightweight multiprocessing library that provides true parallelism for CPU-bound tasks by bypassing Python's Global Interpreter Lock (GIL), enabling full utilization of multi-core processors
- Async/await native design with automatic queue management and worker process lifecycle handling, eliminating the complexity of manual process spawning and inter-process communication
- Built-in context management for sharing expensive resources like database connection pools and HTTP clients across jobs, reducing initialization overhead
- Type-safe configuration using Pydantic for automatic validation of input data, with configurable queue sizes, worker counts, and graceful shutdown handling
- Perfect for CPU-intensive workloads like data processing, image manipulation, scientific computing, and batch operations that need to scale beyond single-threaded execution

### Caching

**[aiocache](https://aiocache.readthedocs.io/) Integration**

- High-performance async caching library with support for multiple backends including Redis, Memcached, and in-memory storage, providing millisecond-level response times for frequently accessed data
- Automatic cache configuration and connection management with separate cache instances for different TTL requirements: default (5 minutes), persistent (1 hour), and custom durations for specific use cases
- Decorator-based caching with `@cached` for effortless function result memoization, automatically serializing complex Python objects including Pydantic models, dataclasses, and custom types
- Built-in cache warming on application startup for Celery workers and web servers, pre-populating critical data to eliminate cold-start latency and ensure consistent performance from the first request
- Type-safe settings configuration for cache behavior including host, port, TTL values, and enable/disable flags, with automatic validation and clear error messages for misconfigurations
- Production-ready Redis integration with connection pooling, automatic reconnection handling, and graceful degradation when cache is unavailable, preventing cascading failures

### Database & ORM

**[SQLAlchemy](https://www.sqlalchemy.org/) + [Alembic](https://alembic.sqlalchemy.org/en/latest/)**

- SQLAlchemy 2.0+ with full async/await support for non-blocking database operations, enabling high-concurrency applications that can handle thousands of simultaneous database connections
- Powerful ORM with relationship mapping, lazy/eager loading strategies, and advanced querying capabilities including joins, subqueries, window functions, and CTEs
- Automatic model discovery and registration system that finds all your database models without explicit imports, simplifying project organization
- Alembic-powered database migration system for version-controlled schema changes, with automatic migration generation by comparing models to database state, rollback support, and team collaboration features
- Built-in connection pool management with configurable pool sizes, overflow handling, connection recycling, and health checks for production reliability

**[Paracelsus](https://github.com/tedivm/paracelsus) Integration**

- Automatic generation of beautiful database schema diagrams in multiple formats (PNG, SVG, PDF) using Graphviz, visualizing tables, columns, and relationships at a glance
- One-command documentation generation that extracts database comments, column types, constraints, and indexes into comprehensive markdown documentation
- Interactive visual representation of foreign key relationships, many-to-many associations, and table hierarchies to help new developers understand your data model quickly

### Command Line Interface

**[Typer](https://typer.tiangolo.com/) + [Click](https://click.palletsprojects.com/)**

- Modern CLI framework built on Click that uses Python type hints to automatically generate command-line interfaces, eliminating boilerplate code and providing excellent IDE support
- Beautiful, colorized terminal output with progress bars, spinners, tables, and rich formatting using the Rich library for professional-looking command-line tools
- Automatic help text generation from docstrings and type annotations, with support for command groups, subcommands, and nested command hierarchies
- Type-safe argument and option definitions with automatic validation, conversion, and helpful error messages when users provide incorrect input
- Full async/await support for commands that need to perform I/O operations, with seamless integration with your async application code
- Shell auto-completion for Bash, Zsh, Fish, and PowerShell, generated automatically from your command definitions to improve developer experience

### Templating

**[Jinja2](https://jinja.palletsprojects.com/) Templates**

- Industry-standard templating engine for generating HTML, XML, emails, and other text formats with Python-like syntax including loops, conditionals, and filters
- Template inheritance and composition with blocks, includes, and macros for building complex page layouts from reusable components while maintaining DRY principles
- Pre-configured custom filters and functions specific to your application domain, with automatic template reloading in development and compilation caching in production
- Built-in XSS protection through automatic HTML escaping, with granular control over when to escape content for security-critical applications
- Seamless integration with FastAPI for server-side rendering, perfect for hybrid applications that combine API endpoints with traditional server-rendered pages

### Containerization

**[Docker](https://www.docker.com/) Setup**

- Complete [Docker Compose](https://docs.docker.com/compose/) orchestration for local development with separate services for web, workers, databases, and caches, enabling full-stack development without complex local installations
- Separate configurations for development (with hot-reload, debug tools, and volume mounts) and production (with security hardening, optimized layers, and minimal dependencies)
- Multi-architecture image builds using [Multi-Py](https://github.com/multi-py/) for seamless deployment on AMD64, ARM64, and Apple Silicon, with automated builds for multiple Python versions

### CI/CD Pipeline

**Comprehensive [GitHub Actions](https://docs.github.com/en/actions)**

- Matrix testing across multiple Python versions (3.10, 3.11, 3.12, 3.13, 3.14) to ensure broad compatibility before release
- Automated code quality enforcement with Ruff for formatting and linting, mypy for type checking, and pytest for test execution
- Fully automated PyPI publishing triggered by git tags, with automatic changelog generation, version bumping, and release notes from commit messages
- Container image building and multi-architecture publishing to GitHub Container Registry and Docker Hub, with automatic tagging based on branches and release/tag versions
- Intelligent dependency updates using Dependabot and [uv](https://pypi.org/project/uv/) lockfile management for fast, reproducible builds and automated PR creation for updates

### AI Development Support

- Pre-configured **AGENTS.md** file following the [open standard](https://agents.md/) adopted by over 20,000 open-source projects and supported by Cursor, Aider, Devin, GitHub Copilot, and other AI coding assistants
- Comprehensive project-specific guidelines including Python version requirements, async/await preferences, typing conventions, security practices, and framework-specific patterns for FastAPI, SQLAlchemy, and Typer
- Detailed best practices for production-ready code including logging strategies, error handling, dependency management, and testing patterns that help AI agents write code matching your team's standards
- Context-aware instructions that automatically adapt based on your selected features, ensuring AI assistants understand your project's architecture, available tools, and development workflows
- Living documentation that serves as both onboarding material for human developers and precise guidance for AI agents, reducing the cognitive load of explaining project conventions repeatedly

## Comprehensive Documentation

Every generated project includes documentation tailored to your selected features:

- **Developer Guide Hub**: Organized documentation index in `docs/dev/` with dedicated guides for each enabled feature
- **FastAPI Documentation**: Integration guide covering static file serving, Docker configuration, and FastAPI dependency system usage
- **Database Documentation**: SQLAlchemy and Alembic guide covering model organization, migration creation using Make commands, FastAPI integration, and automatic schema diagram generation with Paracelsus
- **Caching Documentation**: aiocache integration guide covering cache configuration, decorator usage, multiple TTL strategies, and cache warming for optimal performance
- **Task Processing Guides**: Documentation for Celery (worker and beat configuration, Docker setup) and QuasiQueue (configuration file location, Docker images)
- **CLI Documentation**: Guide showing how to use the generated CLI and where to add new commands
- **Docker Documentation**: Container setup documentation covering image sources, development environment, and registry publishing
- **Settings Documentation**: Guide to the Pydantic Settings configuration system and how to extend the Settings class
- **Dependencies & Testing**: Documentation on dependency management and pytest setup using the Makefile task runner

## Smart Configuration

The template intelligently configures itself based on your choices through sophisticated post-generation hooks:

- **Surgical Dependency Management**: Only includes packages you actually need in `pyproject.toml`, with proper optional dependency groups for dev tools, testing, and feature-specific requirements, avoiding bloated dependency trees
- **Conditional Docker Services**: Automatically generates docker-compose.yaml with only the services your project requires: PostgreSQL for SQLAlchemy, Redis for Celery/aiocache caching, with properly configured health checks, volumes, and networking
- **Cache-Aware Configuration**: When aiocache is enabled, automatically configures Redis connection settings, multiple cache instances with different TTL strategies, and cache warming hooks for FastAPI and Celery startup events
- **Database-Aware Configuration**: Sets up appropriate connection strings, pool sizes, and dialect-specific settings for PostgreSQL or SQLite, with Alembic migrations configured for cross-database compatibility
- **Feature-Driven CI/CD Workflows**: GitHub Actions workflows are conditionally installed based on your feature selection: container building and publishing only when Docker is enabled, PyPI publishing workflow only when configured, eliminating unused automation files from your repository
- **Framework Integration**: Automatically wires together selected components (FastAPI with SQLAlchemy database dependencies, Celery with Redis broker, CLI with async command support) providing working examples of how pieces fit together
- **Intelligent Cleanup**: Post-generation scripts remove unused files, imports, and configuration blocks based on your selections, ensuring you get a clean, minimal codebase with zero dead code or commented-out sections

## Multiple License Options

Choose the license that fits your project:

- **MIT License**: Permissive, business-friendly
- **BSD License**: Simple and permissive
- **Apache Software License 2.0**: Patent protection included
- **GNU General Public License v3**: Copyleft for open source
- **All Rights Reserved**: Proprietary projects

## Project Examples

See the template in action with complete example projects:

**[📖 Library Example](https://github.com/tedivm/robs_awesome_python_template_examples/tree/main/library)**

- Minimal setup for Python libraries
- GitHub Actions, Agentic File, CLI, and PyPI publishing enabled
- Documentation and testing included

**[🚀 Full Application](https://github.com/tedivm/robs_awesome_python_template_examples/tree/main/full)**

- Every feature enabled
- Complete web application with API, database, and task processing
- Production deployment ready

**[⚡ Minimal Setup](https://github.com/tedivm/robs_awesome_python_template_examples/tree/main/bare)**

- Bare minimum configuration with all optional features disabled
- Perfect starting point for simple projects

## Get Started Today

```bash
cookiecutter gh:tedivm/robs_awesome_python_template
```

Your next Python project is just one command away!
