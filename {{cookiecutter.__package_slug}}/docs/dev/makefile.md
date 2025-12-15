# Makefile

This project uses a comprehensive makefile to automate common development tasks including installation, testing, formatting, dependency management, and packaging. The makefile provides a consistent interface for all developers regardless of their environment.

## Shell Autocomplete

**Recommendation**: Enable makefile target autocomplete in your shell to make finding and running targets easier.

**Bash**:

Add to your `~/.bashrc`:

```bash
complete -W "\`grep -oE '^[a-zA-Z0-9_.-]+:([^=]|$)' Makefile | sed 's/[^a-zA-Z0-9_.-]*$//'\`" make
```

**Zsh**:

Add to your `~/.zshrc`:

```zsh
# Enable bash completion compatibility
autoload -U +X bashcompinit && bashcompinit

# Makefile target completion
complete -W "\`grep -oE '^[a-zA-Z0-9_.-]+:([^=]|$)' Makefile | sed 's/[^a-zA-Z0-9_.-]*$//'\`" make
```

**Fish**:

Add to your `~/.config/fish/config.fish`:

```fish
complete -c make -a "(make -qp | awk -F':' '/^[a-zA-Z0-9][^$#\/\t=]*:([^=]|$)/ {split(\$1,A,/ /);for(i in A)print A[i]}')"
```

After adding and sourcing your shell config, you can type `make` followed by `<Tab>` to see all available targets:

```bash
$ make <Tab>
install          pytest           chores           build
tests            ruff_check       black_fixes      dependencies
# ... and more
```

## Overview

The makefile handles:

- Python environment setup and package installation
- Code formatting and linting
- Test execution with coverage
- Type checking with mypy
- Dependency compilation
{%- if cookiecutter.include_sqlalchemy == "y" %}
- Database migrations and schema documentation
{%- endif %}
- Package building

All makefile targets are designed to work in both local development and CI environments.

## Quick Reference

```bash
# Initial setup
make install

# Run all tests and checks
make tests

# Auto-fix formatting issues
make chores

# Run tests with coverage
make pytest

# Build package
make build
```

## Installation Targets

### `make install`

**Purpose**: Complete environment setup for new developers.

**What it does**:

1. Ensures uv is installed
2. Creates a virtual environment using uv (automatically installs Python if needed)
3. Installs the package and all development dependencies using uv

**Usage**:

```bash
# First time setup
make install

# After pulling changes that update dependencies
make install
```

**Notes**:

- Safe to run multiple times (idempotent)
- uv automatically installs the correct Python version from `.python-version`
- Creates `.venv` directory if it doesn't exist
- Much faster than traditional pip installation (10-100x speedup)

### `make sync`

**Purpose**: Install or update Python dependencies.

**What it does**:

- Installs the package in editable mode with development extras using uv
- Updates dependencies if `pyproject.toml` has changed

**Usage**:

```bash
# Update dependencies after pyproject.toml changes
make sync
```

### `make uv`

**Purpose**: Ensure uv is installed.

**What it does**:

- Checks if uv is available on the system
- Installs uv via pip if not found
- This is automatically called by `make install`

**Usage**:

```bash
# Ensure uv is installed (usually not needed directly)
make uv
```

## Formatting Targets

### `make chores`

**Purpose**: Automatically fix all formatting and style issues.

**What it does**:

- Fixes linting issues with Ruff
- Formats code with Black (via Ruff)
- Formats data files with dapperdata
- Sorts TOML files
{%- if cookiecutter.include_sqlalchemy == "y" %}
- Updates database schema documentation
{%- endif %}

**Usage**:

```bash
# Before committing code
make chores
```

**Best Practice**: Run this before committing to ensure code passes CI checks.

### `make ruff_fixes`

**Purpose**: Automatically fix linting issues.

**What it does**:

- Runs Ruff with `--fix` flag
- Fixes issues like unused imports, missing commas, etc.

**Usage**:

```bash
# Fix linting issues
make ruff_fixes
```

### `make black_fixes`

**Purpose**: Format code to Black standard.

**What it does**:

- Runs Ruff's formatter (Black-compatible)
- Formats all Python files consistently

**Usage**:

```bash
# Format all Python files
make black_fixes
```

### `make dapperdata_fixes`

**Purpose**: Format JSON and YAML data files.

**What it does**:

- Pretty-prints JSON files
- Formats YAML files consistently
- Fixes indentation and structure

**Usage**:

```bash
# Format data files
make dapperdata_fixes
```

### `make tomlsort_fixes`

**Purpose**: Sort and format TOML files.

**What it does**:

- Sorts keys in TOML files alphabetically
- Ensures consistent TOML formatting

**Usage**:

```bash
# Sort TOML files
make tomlsort_fixes
```

## Testing Targets

### `make tests`

**Purpose**: Run the complete test suite including all checks.

**What it does**:

1. Ensures dependencies are installed
2. Runs pytest with coverage
3. Checks linting (ruff)
4. Checks formatting (black)
5. Runs type checking (mypy)
6. Checks data file formatting
7. Checks TOML file sorting
{%- if cookiecutter.include_sqlalchemy == "y" %}
8. Verifies database schema documentation is up-to-date
{%- endif %}

**Usage**:

```bash
# Run full test suite (what CI runs)
make tests
```

**Best Practice**: Run this before pushing to ensure CI will pass.

### `make pytest`

**Purpose**: Run pytest with coverage reporting.

**What it does**:

- Executes all tests in the `tests/` directory
- Generates coverage report
- Shows which lines are covered by tests
- Fails if coverage is below threshold

**Usage**:

```bash
# Run tests with coverage
make pytest

# See detailed output
make pytest_loud
```

**Output Example**:

```
tests/test_api.py ........                                           [ 25%]
tests/test_models.py ............                                    [ 75%]
tests/test_services.py ....                                          [100%]

---------- coverage: platform darwin, python 3.12.0 -----------
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
myproject/__init__.py              4      0   100%
myproject/services/cache.py       45      2    96%   78-79
------------------------------------------------------------
TOTAL                            250      2    99%
```

### `make pytest_loud`

**Purpose**: Run pytest with verbose debug logging.

**What it does**:

- Same as `make pytest` but with debug logging enabled
- Shows all log messages during test execution
- Useful for debugging test failures

**Usage**:

```bash
# Debug test failures
make pytest_loud
```

### `make ruff_check`

**Purpose**: Check for linting issues without fixing them.

**What it does**:

- Runs Ruff linter
- Reports issues but doesn't modify files
- Exits with error if issues are found

**Usage**:

```bash
# Check linting
make ruff_check
```

### `make black_check`

**Purpose**: Check code formatting without modifying files.

**What it does**:

- Verifies code matches Black style
- Reports files that would be reformatted
- Exits with error if formatting is needed

**Usage**:

```bash
# Check if code needs formatting
make black_check
```

### `make mypy_check`

**Purpose**: Run static type checking.

**What it does**:

- Analyzes code for type errors
- Checks type hints are correct
- Ensures type consistency across the codebase

**Usage**:

```bash
# Check types
make mypy_check
```

### `make dapperdata_check`

**Purpose**: Check data file formatting without modifying.

**What it does**:

- Verifies JSON/YAML files are properly formatted
- Exits with error if files need formatting

**Usage**:

```bash
# Check data file formatting
make dapperdata_check
```

### `make tomlsort_check`

**Purpose**: Verify TOML files are properly sorted.

**What it does**:

- Checks if TOML files are sorted alphabetically
- Exits with error if sorting is needed

**Usage**:

```bash
# Check TOML sorting
make tomlsort_check
```

## Dependency Management

### `make lock`

**Purpose**: Update the uv.lock lockfile with latest compatible versions.

**What it does**:

- Reads `pyproject.toml` for dependency specifications
- Resolves all dependencies and transitive dependencies
- Generates cross-platform `uv.lock` with exact versions and hashes
- Uses `--upgrade` flag to get latest compatible versions

**Usage**:

```bash
# Update lockfile with latest dependencies
make lock

# After modifying pyproject.toml
make lock
```

**File Generated**:

- `uv.lock` - Cross-platform lockfile with all dependencies, versions, and hashes

### `make lock-check`

**Purpose**: Verify that uv.lock is up-to-date with pyproject.toml.

**What it does**:

- Checks if lockfile needs updating
- Returns error if pyproject.toml changed without updating lock
- Useful in CI/CD to ensure lockfile is committed

**Usage**:

```bash
# Check if lockfile is current
make lock-check
```

**When to Use**:

- In CI/CD pipelines to verify lockfile freshness
- Before committing changes to ensure lock is updated
- When you want the latest compatible versions

## Packaging Targets

### `make build`

**Purpose**: Build distributable package.

**What it does**:

- Creates source distribution (`.tar.gz`)
- Creates wheel distribution (`.whl`)
- Places builds in `dist/` directory

**Usage**:

```bash
# Build package for distribution
make build
```

**Output**:

- `dist/{{cookiecutter.__package_slug}}-X.Y.Z.tar.gz` - Source distribution
- `dist/{{cookiecutter.__package_slug}}-X.Y.Z-py3-none-any.whl` - Wheel distribution
{%- if cookiecutter.include_sqlalchemy == "y" %}

## Database Targets

### `make run_migrations`

**Purpose**: Run all pending database migrations.

**What it does**:

- Executes Alembic migrations to bring database up to date
- Applies all migrations that haven't been run yet
- Updates the database schema

**Usage**:

```bash
# Apply pending migrations
make run_migrations
```

**Best Practice**: Run this after pulling changes that include new migrations.

### `make create_migration`

**Purpose**: Create a new database migration from model changes.

**What it does**:

1. Creates a temporary database
2. Applies all existing migrations
3. Compares current models to database schema
4. Generates migration file for differences
5. Formats the migration file

**Usage**:

```bash
# Create migration with descriptive message
make create_migration MESSAGE="add user profile fields"
```

**Requirements**:

- Must provide a `MESSAGE` parameter
- Message should describe the schema changes

**Output**: Creates a new file in `db/versions/` with the migration code.

**Example**:

```bash
# Add new column
make create_migration MESSAGE="add email column to users"

# Create new table
make create_migration MESSAGE="add products table"

# Modify relationship
make create_migration MESSAGE="update order-product relationship"
```

### `make check_ungenerated_migrations`

**Purpose**: Verify no model changes exist without migrations.

**What it does**:

- Compares current models to latest migration
- Exits with error if unmigrated changes are detected
- Ensures developers create migrations for model changes

**Usage**:

```bash
# Check for missing migrations
make check_ungenerated_migrations
```

**Best Practice**: Run this in CI to catch forgotten migrations.

### `make document_schema`

**Purpose**: Update database schema documentation.

**What it does**:

- Introspects SQLAlchemy models
- Generates schema tables and diagrams
- Injects schema into `docs/dev/database.md`
- Uses Paracelsus to auto-generate documentation

**Usage**:

```bash
# Update schema docs after model changes
make document_schema
```

**Best Practice**: Include this in `make chores` to keep docs current.

### `make paracelsus_check`

**Purpose**: Verify database schema documentation is up-to-date.

**What it does**:

- Checks if schema docs match current models
- Exits with error if docs are outdated
- Doesn't modify any files

**Usage**:

```bash
# Check schema documentation
make paracelsus_check
```

**Best Practice**: Run this in CI to ensure schema docs stay current.

### `make reset_db`

**Purpose**: Clear and recreate the database.

**What it does**:

1. Removes all database files
2. Runs all migrations from scratch
3. Creates a fresh database schema

**Usage**:

```bash
# Reset development database
make reset_db
```

**Warning**: This deletes all data! Only use in development.

### `make clear_db`

**Purpose**: Delete all database files.

**What it does**:

- Removes SQLite database files
- Cleans up journal and WAL files

**Usage**:

```bash
# Delete database files
make clear_db
```

**Warning**: This deletes all data! Only use in development.
{%- endif %}

## Environment Variables

The makefile respects several environment variables:

### `CI`

**Purpose**: Indicates running in CI environment.

**Effect**:

- Uses system Python instead of creating `.venv`
- Adjusts paths for CI environment
- Still uses uv for fast dependency installation

**Usage**:

```bash
# Automatically set by GitHub Actions and other CI systems
CI=true make tests
```

### `USE_SYSTEM_PYTHON`

**Purpose**: Use system Python instead of virtual environment.

**Effect**:

- Skips `.venv` creation
- Installs packages to system Python
- Useful for containers

**Usage**:

```bash
# Use system Python
USE_SYSTEM_PYTHON=true make install
```

{%- if cookiecutter.include_sqlalchemy == "y" %}

### `DATABASE_URL`

**Purpose**: Override database connection URL.

**Effect**:

- Used by Alembic for migrations
- Allows targeting different databases

**Usage**:

```bash
# Run migrations against specific database
DATABASE_URL=postgresql://localhost/mydb make run_migrations
```

{%- endif %}

## Common Workflows

### New Developer Setup

```bash
# 1. Clone repository
git clone <repo-url>
cd <repo>

# 2. Complete setup
make install

# 3. Verify everything works
make tests
```

### Daily Development

```bash
# 1. Pull latest changes
git pull

# 2. Update dependencies if needed
make install

# 3. Make code changes
# ... edit files ...

# 4. Run tests frequently
make pytest

# 5. Fix formatting before committing
make chores

# 6. Run full test suite
make tests

# 7. Commit and push
git add .
git commit -m "Description"
git push
```

{%- if cookiecutter.include_sqlalchemy == "y" %}

### Database Changes

```bash
# 1. Modify models
# ... edit model files ...

# 2. Create migration
make create_migration MESSAGE="describe changes"

# 3. Review generated migration
# ... check db/versions/latest_file.py ...

# 4. Apply migration locally
make run_migrations

# 5. Update schema documentation
make document_schema

# 6. Test migration is reversible
make reset_db

# 7. Commit migration and documentation
git add db/versions/ docs/dev/database.md
git commit -m "Add migration: describe changes"
```

{%- endif %}

### Dependency Updates

```bash
# 1. Update pyproject.toml (if needed)
# ... modify dependencies ...

# 2. Update lockfile
make lock

# 3. Install updated dependencies
make sync

# 4. Run tests to verify compatibility
make tests

# 5. Commit changes
git add pyproject.toml uv.lock
git commit -m "Update dependencies"
```

### Pre-Release Checklist

```bash
# 1. Ensure all tests pass
make tests

# 2. Verify formatting
make chores
{%- if cookiecutter.include_sqlalchemy == "y" %}

# 3. Check for unmigrated changes
make check_ungenerated_migrations
{%- endif %}

# 4. Build package
make build

# 5. Test installation from build
pip install dist/*.whl

# 6. Tag and release
git tag v1.0.0
git push --tags
```

## Makefile Architecture

### Python Environment Detection

The makefile automatically detects the environment:

- **Local Development**: Uses `.venv` with uv for Python version management
- **CI Environment**: Uses system Python with uv for fast dependency installation
- **System Python Mode**: Skips virtual environment

### Target Dependencies

Targets declare dependencies to ensure proper setup:

```makefile
make pytest  # Requires install
make tests   # Requires install + pytest + all checks
make build   # Requires install
```

### Phony Targets

All operational targets are marked as `.PHONY` to ensure they run even if files with those names exist:

```makefile
.PHONY: tests pytest install build
```

## Troubleshooting

### "python: command not found"

**Problem**: Python is not installed or not in PATH.

**Solution**:

```bash
# uv will automatically install Python when you run
make install

# Or install Python via your system package manager
# Then run make install
```

### "make: command not found"

**Problem**: Make is not installed.

**Solution**:

```bash
# macOS
xcode-select --install

# Ubuntu/Debian
sudo apt-get install build-essential

# Fedora/RHEL
sudo dnf install make
```

### "No rule to make target"

**Problem**: Typo in make target or target doesn't exist.

**Solution**:

```bash
# List all available targets
make help  # If available
grep "^[a-zA-Z]" makefile  # Show all targets
```

### Tests fail after pulling changes

**Problem**: Dependencies are out of sync.

**Solution**:

```bash
# Reinstall dependencies
make install

# Run tests again
make tests
```

{%- if cookiecutter.include_sqlalchemy == "y" %}

### Migration fails

**Problem**: Database schema conflict or migration error.

**Solution**:

```bash
# Reset database and try again
make reset_db

# If problem persists, check migration file
# Then create new migration
make create_migration MESSAGE="fix schema issue"
```

{%- endif %}

## Best Practices

1. **Run `make install` first**: Always start with a complete installation

2. **Use `make chores` before committing**: Ensures code passes formatting checks

3. **Run `make tests` before pushing**: Catches issues before CI

4. **Keep dependencies updated**: Run `make dependencies` after changing `pyproject.toml`
{%- if cookiecutter.include_sqlalchemy == "y" %}

5. **Create migrations for model changes**: Always run `make create_migration` after modifying models

6. **Update schema docs**: Include `make document_schema` in your workflow
{%- endif %}

7. **Use specific targets during development**: Run `make pytest` frequently rather than the full `make tests`

8. **Check target dependencies**: Some targets require `make install` to run first

## Integration with CI/CD

The makefile is designed to work seamlessly in CI environments:

**GitHub Actions**:

```yaml
- name: Run tests
  run: make tests
  env:
    CI: true
```

**Key CI Behaviors**:

- Skips pyenv (uses system Python)
- Skips virtual environment creation
- All checks run identically to local
- Exit codes propagate correctly

## References

- [GNU Make Manual](https://www.gnu.org/software/make/manual/)
- [Python Packaging Guide](https://packaging.python.org/)
- [pytest Documentation](https://docs.pytest.org/)
{%- if cookiecutter.include_sqlalchemy == "y" %}
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
{%- endif %}

## See Also

- [Dependencies](./dependencies.md) - Detailed dependency management guide
- [Testing](./testing.md) - Comprehensive testing documentation
{%- if cookiecutter.include_sqlalchemy == "y" %}
- [Database](./database.md) - Database and migration guide
{%- endif %}
{%- if cookiecutter.include_github_actions == "y" %}
- [GitHub Actions](./github.md) - CI/CD workflow documentation
{%- endif %}
