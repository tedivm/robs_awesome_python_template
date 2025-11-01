# 🚀 Rob's Awesome Python Template

**The most comprehensive Python project template that scales from simple libraries to enterprise applications**

Transform any Python idea into a production-ready project in minutes. This CookieCutter template provides everything you need to build, test, deploy, and maintain modern Python applications with industry best practices baked in.

## ✨ Why Choose This Template?

- **Zero Configuration Hassle**: Get a fully configured development environment instantly
- **Production Ready**: Battle-tested tools and patterns used in real-world applications
- **Incredibly Flexible**: Mix and match features to create exactly what you need
- **Modern Standards**: Uses the latest Python tooling and best practices
- **Enterprise Grade**: Scales from weekend projects to mission-critical applications

## 🎯 Quick Start

```bash
# Install cookiecutter if you haven't already
pip install cookiecutter

# Create your project
cookiecutter gh:tedivm/robs_awesome_python_template
```

Answer a few questions about your project, and you'll have a complete Python application with everything configured and ready to go!

## 🏗️ Core Features (Always Included)

Every project created with this template includes these essential components:

**Development Tools**

- **[Makefile](https://www.gnu.org/software/make/manual/html_node/Introduction.html) automation**: One-command setup, testing, and deployment
- **Modern pyproject.toml**: No legacy setup.py files
- **Virtual environment management**: Automatic venv setup with [pyenv](https://github.com/pyenv/pyenv) integration
- **[Pre-commit](https://pre-commit.com/) hooks**: Catch issues before they reach your repository

**Code Quality**

- **[Ruff](https://docs.astral.sh/ruff/)**: Lightning-fast formatting and linting
- **[mypy](https://mypy.readthedocs.io/en/stable/)**: Static type checking for safer code
- **[pytest](https://docs.pytest.org/)**: Comprehensive testing framework with async support
- **Coverage reporting**: Track your test coverage (even with multiprocess applications)

**Configuration & Settings**

- **[Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)**: Type-safe configuration management
- **Environment-based config**: Easy deployment across different environments
- **Automatic validation**: Catch configuration errors early

**Publishing & Distribution**

- **[setuptools-scm](https://pypi.org/project/setuptools-scm/)**: Automatic versioning from git tags
- **PyPI publishing**: One-command package publishing
- **Multi-architecture support**: Works on AMD64 and ARM64

## 🧩 Optional Integrations

Pick and choose the features you need. Unused components are completely removed from your project.

### 🌐 Web Applications

**[FastAPI](https://fastapi.tiangolo.com/) Integration**

- Complete REST API setup with automatic documentation
- Static file serving
- Async request handling
- OpenAPI/Swagger UI included
- Production-ready ASGI configuration

### 📋 Task Processing

**[Celery](https://docs.celeryq.dev/en/stable/) Integration**

- Distributed task queue setup
- [Redis](https://redis.io/) broker configuration
- Worker and scheduler containers
- Monitoring and management tools

**[QuasiQueue](https://github.com/tedivm/quasiqueue) Integration**

- High-performance multiprocessing
- Simple async task processing
- Perfect for CPU-intensive workloads

### 💾 Database & ORM

**[SQLAlchemy](https://www.sqlalchemy.org/) + [Alembic](https://alembic.sqlalchemy.org/en/latest/)**

- Async database operations
- Automatic model discovery
- Database migration management
- Support for PostgreSQL, SQLite, and more
- Connection pooling and optimization

**[Paracelsus](https://github.com/tedivm/paracelsus) Integration**

- Automatic database schema diagrams
- Documentation generation
- Visual database relationships

### 🖥️ Command Line Interface

**[Typer](https://typer.tiangolo.com/) + [Click](https://click.palletsprojects.com/)**

- Beautiful CLI applications
- Automatic help generation
- Type-safe command definitions
- Async command support
- Auto-completion support

### 🎨 Templating

**[Jinja2](https://jinja.palletsprojects.com/) Templates**

- Server-side rendering
- Template inheritance
- Custom filters and functions

### 🐳 Containerization

**[Docker](https://www.docker.com/) Setup**

- Multi-service [Docker Compose](https://docs.docker.com/compose/) configuration
- Optimized multi-stage builds
- Development and production configurations
- Health checks and resource limits
- Multi-architecture image support from [Multi-Py](https://github.com/multi-py/)

### ⚙️ CI/CD Pipeline

**Comprehensive [GitHub Actions](https://docs.github.com/en/actions)**

- Automated testing across Python versions
- Code formatting and linting
- Type checking with mypy
- Security scanning
- Automated PyPI publishing
- Container image building and publishing
- Dependency updates with [uv](https://pypi.org/project/uv/) lockfile management
- Documentation generation and deployment

### 🤖 AI Development Support

**Agentic Instructions**

- Pre-configured AGENTS.md with project-specific guidelines
- Best practices for AI coding assistants
- Context-aware development workflows

## 📚 Comprehensive Documentation

Every generated project includes extensive documentation:

- **API Documentation**: Auto-generated from code
- **Development Guides**: Database, caching, CLI, Docker setups
- **Deployment Instructions**: Production deployment strategies

## 🎛️ Smart Configuration

The template intelligently configures itself based on your choices:

- **Dependency management**: Only includes what you need
- **Docker services**: Automatically sets up required containers
- **Database connections**: Configures based on selected databases
- **CI/CD workflows**: Enables relevant automation pipelines
- **Settings management**: Creates environment-specific configurations

## 🎨 Multiple License Options

Choose the license that fits your project:

- **MIT License**: Permissive, business-friendly
- **BSD License**: Simple and permissive
- **Apache Software License 2.0**: Patent protection included
- **GNU General Public License v3**: Copyleft for open source
- **All Rights Reserved**: Proprietary projects

## 📦 Project Examples

See the template in action with complete example projects:

**[📖 Library Example](https://github.com/tedivm/robs_awesome_python_template_examples/tree/main/library)**

- Minimal setup for Python packages
- PyPI publishing ready
- Documentation and testing included

**[🚀 Full Application](https://github.com/tedivm/robs_awesome_python_template_examples/tree/main/full)**

- Every feature enabled
- Complete web application with API, database, and task processing
- Production deployment ready

**[⚡ Minimal Setup](https://github.com/tedivm/robs_awesome_python_template_examples/tree/main/bare)**

- Bare minimum configuration
- Perfect starting point for simple projects

## 🔧 Advanced Features

**Intelligent Cleanup**

- Unused files and configurations are automatically removed
- No bloat or unnecessary dependencies
- Clean, focused project structure

**Development Workflow**

- One-command environment setup
- Automated testing and formatting
- Integrated debugging support
- Hot-reload for web applications

**Production Ready**

- Environment-based configuration
- Health checks and monitoring
- Optimized Docker containers

## 🚀 Get Started Today

```bash
cookiecutter gh:tedivm/robs_awesome_python_template
```

Your next Python project is just one command away!
