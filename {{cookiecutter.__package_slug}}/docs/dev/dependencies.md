# Dependencies

This project uses modern Python packaging standards with `pyproject.toml` as the central configuration file for all dependencies, build settings, and tool configurations.

## Dependency Management Structure

Dependencies are organized in `pyproject.toml` using the modern Python packaging standard (PEP 621):

```toml
[project]
name = "{{cookiecutter.__package_slug}}"
dependencies = [
  # Runtime dependencies required to run the application
]

[project.optional-dependencies]
dev = [
  # Development dependencies for testing, linting, etc.
]
```

### Main Dependencies vs Dev Dependencies

**Main Dependencies** (`dependencies`):

- Required to run the application in production
- Installed with `pip install {{cookiecutter.__package_slug}}`
- Includes frameworks, libraries, and runtime requirements
- Example: `fastapi`, `sqlalchemy`, `pydantic`

**Dev Dependencies** (`optional-dependencies.dev`):

- Only needed during development and testing
- Installed with `pip install {{cookiecutter.__package_slug}}[dev]`
- Includes testing tools, linters, formatters, and build tools
- Example: `pytest`, `ruff`, `mypy`

## Project Dependencies

### Core Runtime Dependencies

All projects include these essential dependencies:

- **pydantic~=2.0**: Data validation and settings management using Python type annotations
- **pydantic-settings**: Extension for loading configuration from environment variables

{%- if cookiecutter.include_fastapi == "y" %}

### Web Framework

- **fastapi**: Modern, high-performance web framework for building APIs with automatic validation and documentation
{%- endif %}

{%- if cookiecutter.include_sqlalchemy == "y" %}

### Database

- **SQLAlchemy**: Comprehensive SQL toolkit and ORM for database operations
- **alembic**: Database migration tool for SQLAlchemy
- **aiosqlite**: Async SQLite driver for development and testing
- **asyncpg**: High-performance async PostgreSQL driver for production
- **psycopg2-binary**: Traditional PostgreSQL adapter (synchronous operations)
{%- endif %}

{%- if cookiecutter.include_celery == "y" %}

### Task Queue

- **celery**: Distributed task queue for asynchronous job processing
- **redis**: Redis client library for Celery broker and result backend
{%- endif %}

{%- if cookiecutter.include_aiocache == "y" %}

### Caching

- **aiocache**: Async caching library supporting multiple backends (Redis, in-memory)
- **redis**: Redis client for cache persistence
{%- endif %}

{%- if cookiecutter.include_jinja2 == "y" %}

### Templating

- **jinja2**: Powerful template engine for generating HTML, configuration files, etc.
{%- endif %}

{%- if cookiecutter.include_quasiqueue == "y" %}

### Multiprocessing

- **QuasiQueue**: Async-native multiprocessing library for CPU-intensive tasks
{%- endif %}

{%- if cookiecutter.include_cli == "y" %}

### CLI

- **typer**: Modern CLI framework based on Python type hints with automatic help generation
{%- endif %}

### Development Dependencies

Development dependencies are organized in the `[project.optional-dependencies]` section:

- **pytest**: Testing framework with powerful fixtures and assertion introspection
- **pytest-asyncio**: Plugin for testing async/await code
- **pytest-cov**: Code coverage reporting plugin
- **pytest-pretty**: Beautiful test output formatting
- **ruff**: Fast Python linter and formatter (replaces Black, isort, Flake8)
- **mypy**: Static type checker for catching type-related bugs
- **build**: PEP 517 build frontend for creating distribution packages
- **dapperdata**: Data formatting and validation tool
- **glom**: Nested data access and transformation
- **greenlet**: Lightweight concurrent programming support (required for coverage with async)
- **toml-sort**: Automatic TOML file sorting for consistency
{%- if cookiecutter.include_fastapi == "y" %}
- **httpx**: Modern HTTP client for testing FastAPI endpoints
{%- endif %}
{%- if cookiecutter.include_sqlalchemy == "y" %}
- **paracelsus**: Automatic database schema documentation generator
{%- endif %}
{%- if cookiecutter.include_requirements_files == "y" %}
- **uv**: Fast Python package installer and resolver for generating requirements files
{%- endif %}

## Adding New Dependencies

### Add Runtime Dependency

Edit `pyproject.toml` and add to the `dependencies` list:

```toml
[project]
dependencies = [
  "requests",  # Add new dependency
  "pydantic~=2.0",
  # ... other dependencies
]
```

Then install:

```bash
# Install with pip
pip install -e .

# Or use make
make install
```

### Add Development Dependency

Edit `pyproject.toml` and add to the `dev` list:

```toml
[project.optional-dependencies]
dev = [
  "black",  # Add new dev dependency
  "pytest",
  # ... other dev dependencies
]
```

Then install:

```bash
# Install with dev dependencies
pip install -e .[dev]

# Or use make
make install
```

### Using pip Directly

You can also add dependencies using pip and then update `pyproject.toml`:

```bash
# Install a package
pip install requests

# Manually add to pyproject.toml dependencies list
# Then reinstall to ensure consistency
pip install -e .[dev]
```

## Removing Dependencies

1. Remove the dependency from `pyproject.toml`
2. Reinstall the package:

```bash
pip install -e .[dev]
```

3. Verify the dependency is removed:

```bash
pip list | grep package-name
```

4. If needed, explicitly uninstall:

```bash
pip uninstall package-name
```

## Version Pinning Strategies

### Compatible Release (Recommended)

Use the `~=` operator for compatible versions:

```toml
"pydantic~=2.0"  # Allows >=2.0.0, <3.0.0
```

**Benefits**:

- Gets bug fixes and minor updates automatically
- Avoids breaking changes from major version bumps
- Balance between stability and updates

### Minimum Version

Specify only minimum version:

```toml
"requests>=2.28.0"  # Any version >= 2.28.0
```

**Use cases**:

- When you need a specific feature added in a version
- Maximum flexibility for dependency resolution

### Exact Version (Not Recommended)

Pin to an exact version:

```toml
"requests==2.31.0"  # Only version 2.31.0
```

**Use cases**:

- Troubleshooting version-specific bugs
- Temporary pin during debugging
- **Warning**: Prevents security updates and bug fixes

### Version Range

Specify a range:

```toml
"django>=4.0,<5.0"  # Version 4.x only
```

### Best Practice

For most dependencies, use compatible release (`~=`):

```toml
dependencies = [
  "pydantic~=2.0",      # Get 2.x updates, avoid 3.x
  "fastapi~=0.109",     # Get 0.109.x updates
  "sqlalchemy~=2.0",    # Get 2.x updates
]
```

{%- if cookiecutter.include_requirements_files == "y" %}

## Requirements Files

This project can optionally generate `requirements.txt` files for compatibility with tools that don't support `pyproject.toml`:

### Generate Requirements Files

```bash
# Generate both requirements files
make dependencies

# Or manually:
make rebuild_dependencies
```

This creates:

- `requirements.txt`: Runtime dependencies only
- `requirements-dev.txt`: Runtime + development dependencies

### How It Works

Uses [uv](https://github.com/astral-sh/uv) for fast dependency resolution:

```bash
# Generate runtime requirements
uv pip compile --output-file=requirements.txt pyproject.toml

# Generate dev requirements
uv pip compile --extra=dev --output-file=requirements-dev.txt pyproject.toml
```

### When to Use Requirements Files

**Use `pyproject.toml`** (preferred):

- Modern Python projects
- Publishing to PyPI
- Editable installs (`pip install -e .`)

**Use `requirements.txt`**:

- Legacy CI/CD systems
- Docker images (for layer caching optimization)
- Tools that don't support pyproject.toml
- Exact reproducible environments

### Installing from Requirements Files

```bash
# Install runtime requirements
pip install -r requirements.txt

# Install dev requirements
pip install -r requirements-dev.txt
```

{%- endif %}

## Updating Dependencies

### Update All Dependencies

```bash
# Update all packages to latest compatible versions
pip install --upgrade -e .[dev]

# Verify updates
pip list --outdated
```

{%- if cookiecutter.include_requirements_files == "y" %}

### Rebuild Requirements Files with Updates

```bash
# Force update of all dependencies in requirements files
make rebuild_dependencies
```

{%- endif %}

### Update Specific Dependency

```bash
# Update one package
pip install --upgrade package-name

# Verify new version
pip show package-name
```

### Check for Outdated Packages

```bash
# List all outdated packages
pip list --outdated

# Show detailed information
pip list --outdated --format=columns
```

## Security Considerations

### Security Scanning

Regularly scan for security vulnerabilities:

```bash
# Using pip-audit (install separately)
pip install pip-audit
pip-audit

# Using safety (install separately)
pip install safety
safety check
```

### Keeping Dependencies Updated

1. **Regular updates**: Update dependencies monthly
2. **Security patches**: Apply security updates immediately
3. **Test thoroughly**: Run full test suite after updates
4. **Review changelogs**: Check breaking changes before major version updates

### Dependabot Integration

{%- if cookiecutter.include_github_actions == "y" %}

This project includes GitHub's Dependabot for automatic dependency updates:

- Automatically creates PRs for dependency updates
- Checks for security vulnerabilities
- Configured in `.github/dependabot.yml`

See [GitHub Actions Documentation](./github.md) for more details.
{%- endif %}

## Virtual Environment Management

### Creating a Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Or using make
make install
```

### Activating the Virtual Environment

```bash
# On macOS/Linux
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

### Using pyenv for Python Version Management

This project uses pyenv to manage Python versions:

```bash
# Install Python version specified in .python-version
make pyenv

# Or manually
pyenv install $(cat .python-version)

# Set local Python version
pyenv local 3.11.0
```

### Checking Virtual Environment

```bash
# Verify you're in the virtual environment
which python
# Should show: /path/to/project/.venv/bin/python

# Check installed packages
pip list

# Check Python version
python --version
```

### Deactivating Virtual Environment

```bash
deactivate
```

## Dependency Resolution Conflicts

### Common Conflicts

When pip cannot resolve dependencies:

```bash
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behavior is the source of the following dependency conflicts.
```

### Troubleshooting Steps

1. **Update pip**:

   ```bash
   pip install --upgrade pip
   ```

2. **Check for incompatible versions**:

   ```bash
   pip check
   ```

3. **Create fresh virtual environment**:

   ```bash
   rm -rf .venv
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .[dev]
   ```

4. **Install dependencies one at a time**:

   ```bash
   pip install pydantic
   pip install fastapi
   # etc.
   ```

5. **Check for pre-release versions**:

   ```bash
   # Allow pre-release versions if needed
   pip install --pre package-name
   ```

### Using pip-compile for Locking

For exact reproducibility, use pip-compile (pip-tools):

```bash
# Install pip-tools
pip install pip-tools

# Generate locked requirements
pip-compile pyproject.toml --output-file=requirements.lock

# Install from locked file
pip install -r requirements.lock
```

## Development vs Production Dependencies

### Development Installation

```bash
# Install with all dev dependencies
pip install -e .[dev]

# Or use make
make install
```

**Includes**:

- Testing frameworks (pytest)
- Linting and formatting (ruff, mypy)
- Build tools
- Documentation generators

### Production Installation

```bash
# Install only runtime dependencies
pip install .

# Or from PyPI
pip install {{cookiecutter.__package_slug}}
```

**Includes**:

- Only dependencies needed to run the application
- Smaller installation size
- Faster installation time

### Docker Production Images

Production Docker images should only install runtime dependencies:

```dockerfile
# Install only runtime dependencies (no [dev])
RUN pip install --no-cache-dir -r requirements.txt
```

## Optional Dependency Groups

You can create multiple optional dependency groups:

```toml
[project.optional-dependencies]
dev = [
  "pytest",
  "ruff",
]

docs = [
  "sphinx",
  "sphinx-rtd-theme",
]

performance = [
  "uvloop",
  "orjson",
]
```

Install specific groups:

```bash
# Install dev dependencies
pip install -e .[dev]

# Install multiple groups
pip install -e .[dev,docs]

# Install all optional dependencies
pip install -e .[dev,docs,performance]
```

## Build System Configuration

The build system is configured at the top of `pyproject.toml`:

```toml
[build-system]
build-backend = "setuptools.build_meta"
requires = ["setuptools>=67.0", "setuptools_scm[toml]>=7.1"]
```

**Components**:

- **build-backend**: Uses setuptools for building packages
- **setuptools**: Modern Python build system
- **setuptools_scm**: Automatic versioning from git tags

### Building Distribution Packages

```bash
# Build source and wheel distributions
make build

# Or manually
python -m build

# Creates:
# dist/{{cookiecutter.__package_slug}}-X.Y.Z.tar.gz (source)
# dist/{{cookiecutter.__package_slug}}-X.Y.Z-py3-none-any.whl (wheel)
```

## Best Practices

1. **Use pyproject.toml as single source of truth**: Don't mix with `setup.py` or `setup.cfg`

2. **Pin major versions with ~=**: Allows updates while preventing breaking changes

   ```toml
   "pydantic~=2.0"  # Good
   "pydantic"       # Bad - no version constraint
   "pydantic==2.5.0"  # Bad - too restrictive
   ```

3. **Separate runtime and dev dependencies**: Keep production images lean

4. **Use editable installs for development**: `-e` flag for faster iteration

   ```bash
   pip install -e .[dev]
   ```

5. **Keep dependencies updated**: Regular updates prevent security issues

6. **Test after updates**: Run full test suite after dependency updates

   ```bash
   pip install --upgrade -e .[dev]
   make test
   ```

7. **Document why dependencies are needed**: Add comments in pyproject.toml

   ```toml
   dependencies = [
     "pydantic~=2.0",  # Settings and validation
     "requests~=2.31",  # HTTP client for external APIs
   ]
   ```

8. **Use virtual environments**: Always work in virtual environments

9. **Lock dependencies for production**: Use requirements files or pip-compile for exact reproducibility

10. **Review dependency licenses**: Ensure compatibility with your project's license

## Troubleshooting

### "ModuleNotFoundError" After Adding Dependency

```bash
# Reinstall to pick up new dependencies
pip install -e .[dev]

# Verify package is installed
pip show package-name
```

### "No module named 'setuptools_scm'"

```bash
# Update pip and install build dependencies
pip install --upgrade pip setuptools wheel
pip install -e .[dev]
```

### Slow Dependency Resolution

```bash
# Use uv for faster dependency resolution
pip install uv
uv pip install -e .[dev]
```

### Conflicting Dependencies

```bash
# Show dependency tree
pip install pipdeptree
pipdeptree

# Find conflicts
pipdeptree --warn conflicts
```

## References

- [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [pip Documentation](https://pip.pypa.io/)
- [pyenv Documentation](https://github.com/pyenv/pyenv)
- [uv - Fast Python Package Installer](https://github.com/astral-sh/uv)
