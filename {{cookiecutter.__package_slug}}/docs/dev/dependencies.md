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

## Lockfile Management

This project uses `uv.lock` for deterministic, reproducible dependency resolution across all environments.

### What is uv.lock?

The `uv.lock` file is a cross-platform lockfile that:

- **Pins exact versions** of all dependencies and transitive dependencies
- **Supports multiple platforms** (Linux, macOS, Windows, ARM64, AMD64)
- **Ensures reproducibility** across development, CI, and production
- **Faster than pip-tools** with built-in conflict resolution
- **Version controlled** - should be committed to git

### Generate/Update Lockfile

```bash
# Update lockfile with latest compatible versions
make lock

# Or manually:
uv lock --upgrade

# Check if lockfile is up-to-date
make lock-check
```

### How It Works

uv reads `pyproject.toml` and generates a comprehensive lockfile:

```bash
# Generate lockfile from pyproject.toml
uv lock

# Update all dependencies to latest compatible versions
uv lock --upgrade

# Verify lockfile is in sync with pyproject.toml
uv lock --check
```

### Installing from Lockfile

**Development** (with dev dependencies):

```bash
# Install from lockfile with dev dependencies
make sync
# Or: uv sync --extra dev
```

**Production** (no dev dependencies):

```bash
# Install from lockfile without dev dependencies
uv sync --frozen --no-dev

# Docker uses this for production images
```

### Why use uv.lock?

**Advantages over requirements.txt**:

- **Multi-platform**: Single file works on Linux, macOS, Windows, ARM64, AMD64
- **Faster resolution**: Rust-powered performance for lockfile generation
- **Better conflict detection**: Catches dependency conflicts earlier
- **Complete dependency tree**: Includes all transitive dependencies with hashes
- **Integrated workflow**: Seamless integration with uv commands

{%- endif %}

## Updating Dependencies

### Update All Dependencies

```bash
# Update lockfile with latest compatible versions
make lock

# Or manually
uv lock --upgrade

# Then sync to install updated dependencies
make sync
```

{%- if cookiecutter.include_requirements_files == "y" %}

### Regenerate Lockfile After Changes

```bash
# After modifying pyproject.toml
make lock
```

{%- endif %}

### Update Specific Dependency

To update a specific package, modify its version constraint in `pyproject.toml`, then:

```bash
# Update lockfile
make lock

# Install the update
make sync
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
# Create virtual environment with uv (automatically installs Python if needed)
uv venv

# Or using make (recommended)
make install
```

uv will automatically:

- Read the Python version from `.python-version`
- Download and install that Python version if not present
- Create a virtual environment in `.venv`

### Activating the Virtual Environment

```bash
# On macOS/Linux
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

### Using uv for Python Version Management

This project uses uv to manage Python versions and virtual environments:

```bash
# uv automatically installs the correct Python version when creating venv
make install

# Or manually create venv with specific Python version
uv venv --python $(cat .python-version)

# uv will download and install Python if not present
```

uv provides several advantages over traditional tools:

- **Automatic Python installation**: No need for separate pyenv setup
- **10-100x faster**: Rust-powered performance for package installation
- **Drop-in pip replacement**: Compatible with existing workflows
- **Built-in virtual environments**: Integrated venv management

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

1. **Update uv**:

   ```bash
   pip install --upgrade uv
   # Or reinstall via the installer
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Check for incompatible versions**:

   ```bash
   uv pip check
   ```

3. **Create fresh virtual environment**:

   ```bash
   rm -rf .venv
   uv venv
   source .venv/bin/activate
   uv pip install -e .[dev]
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
# Install with all dev dependencies using uv
uv pip install -e .[dev]

# Or use make (recommended)
make install
```

**Includes**:

- Testing frameworks (pytest)
- Linting and formatting (ruff, mypy)
- Build tools
- Documentation generators

### Production Installation

```bash
# Install only runtime dependencies using uv
uv pip install .

# Or from PyPI
uv pip install {{cookiecutter.__package_slug}}

# Traditional pip also works
pip install {{cookiecutter.__package_slug}}
```

**Includes**:

- Only dependencies needed to run the application
- Smaller installation size
- Faster installation time

### Docker Production Images

Production Docker images use uv for faster installation:

```dockerfile
# Install uv for fast package installation
RUN pip install --no-cache-dir uv

# Install only runtime dependencies (no [dev])
RUN uv pip install --system --no-cache -r /requirements.txt
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
uv pip install -e .[dev]

# Install multiple groups
uv pip install -e .[dev,docs]

# Install all optional dependencies
uv pip install -e .[dev,docs,performance]
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
uv pip install -e .[dev]

# Verify package is installed
uv pip show package-name
```

### "No module named 'setuptools_scm'"

```bash
# Update uv and install build dependencies
pip install --upgrade uv
uv pip install -e .[dev]
```

### uv Not Found

```bash
# Install uv via pip
pip install uv

# Or use the standalone installer (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex
```

### Conflicting Dependencies

```bash
# Show dependency tree
uv pip install pipdeptree
pipdeptree

# Find conflicts
pipdeptree --warn conflicts
```

## Why uv?

This project uses [uv](https://docs.astral.sh/uv/) as the primary package manager for several compelling reasons:

### Performance

- **10-100x faster** than pip for package installation
- Written in Rust for maximum performance
- Parallel downloads and installations
- Advanced caching strategies

### Convenience

- **Automatic Python management**: Downloads and installs Python versions as needed
- **Drop-in pip replacement**: Compatible with existing pip commands
- **Integrated virtual environments**: Built-in venv management
- **Cross-platform**: Works on Linux, macOS, and Windows

### Reliability

- **Better dependency resolution**: More accurate conflict detection
- **Lockfile generation**: Create reproducible environments
- **Offline mode**: Cache packages for offline installation

### Commands Comparison

| Task | pip | uv |
|------|-----|-----|
| Install package | `pip install package` | `uv pip install package` |
| Create venv | `python -m venv .venv` | `uv venv` |
| Install Python | Requires pyenv/installer | `uv venv --python 3.14` (auto-downloads) |
| Compile requirements | Requires pip-tools | `uv pip compile` (built-in) |
| Speed | Baseline | 10-100x faster |

## References

- [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [uv GitHub Repository](https://github.com/astral-sh/uv)
