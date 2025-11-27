# GitHub Actions

This project includes comprehensive GitHub Actions workflows for automated testing, linting, building, and deployment. Every push and pull request is automatically validated to ensure code quality and functionality.

## Available Workflows

The project includes the following GitHub Actions workflows in `.github/workflows/`:

### Testing Workflows

**pytest.yaml** - Test Suite

- **Trigger**: Every push and pull request
- **Purpose**: Runs the full test suite with coverage reporting
- **Matrix**: Tests against Python 3.10, 3.11, 3.12, 3.13, and 3.14
- **Command**: `make pytest`

### Code Quality Workflows

**ruff.yaml** - Linting

- **Trigger**: Every push and pull request
- **Purpose**: Checks code follows linting rules (code quality, style violations, unused imports, etc.)
- **Command**: `make ruff_check`
- **Note**: Ruff handles linting only; formatting is checked by black.yaml

**black.yaml** - Code Formatting

- **Trigger**: Every push and pull request
- **Purpose**: Enforces Black formatting standard using Ruff as the formatter
- **Command**: `make black_check`
- **Note**: Black is the formatting standard; Ruff is the tool that enforces it

**mypy.yaml** - Type Checking

- **Trigger**: Every push and pull request
- **Purpose**: Validates type hints and catches type-related errors
- **Command**: `make mypy_check`

**dapperdata.yaml** - Data Format Validation

- **Trigger**: Every push and pull request
- **Purpose**: Validates data file formatting (YAML, JSON, etc.)
- **Command**: `make dapperdata_check`

**tomlsort.yaml** - TOML File Sorting

- **Trigger**: Every push and pull request
- **Purpose**: Ensures TOML files (like pyproject.toml) are properly sorted
- **Command**: `make tomlsort_check`

{%- if cookiecutter.include_sqlalchemy == "y" %}

### Database Workflows

**alembic.yaml** - Migration Validation

- **Trigger**: Every push and pull request
- **Purpose**: Ensures all database model changes have corresponding migrations
- **Command**: `make check_ungenerated_migrations`
- **Failure**: Indicates model changes without a migration

**paracelsus.yaml** - Schema Documentation

- **Trigger**: Every push and pull request
- **Purpose**: Validates database schema documentation is up-to-date
- **Command**: `make paracelsus_check`
{%- endif %}

{%- if cookiecutter.include_requirements_files == "y" %}

### Dependency Workflows

**lockfiles.yaml** - Requirements File Validation

- **Trigger**: Every push and pull request
- **Purpose**: Ensures requirements.txt files are synchronized with pyproject.toml
- **Command**: `make dependencies`
{%- endif %}

{%- if cookiecutter.include_docker == "y" %}

### Build and Deployment Workflows

**docker.yaml** - Container Image Publishing

- **Trigger**:
  - Pull requests (build only, no push)
  - Pushes to `main` branch
  - Version tags (v*.*.*)
- **Purpose**: Builds and publishes Docker images to GitHub Container Registry
- **Images**:
{%- if cookiecutter.include_fastapi == "y" %}
  - `ghcr.io/{{cookiecutter.github_org}}/{{cookiecutter.__package_slug}}.www` - FastAPI web server
{%- endif %}
{%- if cookiecutter.include_celery == "y" %}
  - `ghcr.io/{{cookiecutter.github_org}}/{{cookiecutter.__package_slug}}.celery` - Celery workers
{%- endif %}
- **Platforms**: linux/amd64, linux/arm64 (multi-architecture support)
- **Tags**:
  - `main` - Latest development version
  - `pr-N` - Pull request builds
  - `v1.2.3` - Semantic version tags
  - `v1.2`, `v1` - Major/minor version aliases
{%- endif %}

{%- if cookiecutter.publish_to_pypi == "y" %}

**pypi.yaml** - PyPI Package Publishing

- **Trigger**:
  - All pushes and pull requests (build only)
  - Version tags `v*.*.*` (build and publish)
- **Purpose**: Builds Python wheel and publishes to PyPI
- **Authentication**: Uses PyPI Trusted Publishers (OIDC, no tokens needed)
- **Permissions**: Requires `id-token: write` for trusted publishing
{%- endif %}

## Workflow Triggers

### Push Events

Workflows trigger on pushes to any branch:

```yaml
on:
  push:
```

Most workflows run on every push to ensure code quality at all times.

### Pull Request Events

All quality checks run on pull requests:

```yaml
on:
  pull_request:
```

This ensures new code meets quality standards before merging.

### Tag Events

Publishing workflows trigger on version tags:

```yaml
on:
  push:
    tags:
      - "v*.*.*"  # Matches v1.0.0, v2.1.3, etc.
```

Create a tag to trigger a release:

```bash
git tag v1.0.0
git push origin v1.0.0
```

### Branch-Specific Triggers

Some workflows only run on specific branches:

```yaml
on:
  push:
    branches:
      - main
```

## Configuring Secrets

{%- if cookiecutter.publish_to_pypi == "y" %}

### PyPI Publishing (Trusted Publishers)

This project uses PyPI's Trusted Publisher feature, which doesn't require manual API tokens:

1. **On PyPI**:
   - Go to your project on PyPI
   - Navigate to "Publishing" settings
   - Add GitHub as a trusted publisher:
     - Owner: `{{cookiecutter.github_org}}`
     - Repository: `{{cookiecutter.__package_slug}}`
     - Workflow: `pypi.yaml`
     - Environment: (leave blank)

2. **No GitHub Secrets Needed**: The workflow uses OIDC authentication automatically

For more details, see [PyPI Trusted Publishers Documentation](https://docs.pypi.org/trusted-publishers/).
{%- endif %}

### Docker Registry (Automatic)

Docker image publishing uses `GITHUB_TOKEN` which is automatically provided by GitHub Actions. No manual configuration needed.

### Custom Secrets

To add custom secrets:

1. Go to your repository on GitHub
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add your secret name and value

Use secrets in workflows:

```yaml
steps:
  - name: Use Secret
    env:
      MY_SECRET: {% raw %}${{ secrets.MY_SECRET }}{% endraw %}
    run: echo "Using secret"
```

## Branch Protection Rules

Configure branch protection for `main` to require passing checks:

1. Go to Settings → Branches
2. Add branch protection rule for `main`
3. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - Select required status checks:
     - pytest
     - ruff
     - mypy
     {%- if cookiecutter.include_sqlalchemy == "y" %}
     - alembic
     - paracelsus
     {%- endif %}

This prevents merging code that fails tests or quality checks.

## Automated Releases

### Creating a Release

1. **Update version** (optional - setuptools-scm handles this automatically):

   ```bash
   git tag v1.2.3
   ```

2. **Push the tag**:

   ```bash
   git push origin v1.2.3
   ```

3. **Automated actions**:
   {%- if cookiecutter.publish_to_pypi == "y" %}
   - Builds Python package
   - Publishes to PyPI
   {%- endif %}
   {%- if cookiecutter.include_docker == "y" %}
   - Builds Docker images
   - Publishes to GitHub Container Registry with version tags
   {%- endif %}

### Version Tag Format

Use semantic versioning for tags:

- `v1.0.0` - Major release
- `v1.1.0` - Minor release
- `v1.1.1` - Patch release

The `v` prefix is required for workflows to trigger.

### Automated Versioning with setuptools-scm

This project uses `setuptools-scm` for automatic versioning:

- Version derived from git tags
- Commit count added for development versions
- No manual version updates needed

```bash
# Check current version
python -c "from {{cookiecutter.__package_slug}}._version import version; print(version)"

# Development version format: 1.2.3.dev4+g5f8a7bc
# Released version format: 1.2.3
```

{%- if cookiecutter.include_docker == "y" %}

## Container Image Publishing

### Image Naming

Images are published to GitHub Container Registry (GHCR):

{%- if cookiecutter.include_fastapi == "y" %}

- `ghcr.io/{{cookiecutter.github_org}}/{{cookiecutter.__package_slug}}.www`
{%- endif %}
{%- if cookiecutter.include_celery == "y" %}
- `ghcr.io/{{cookiecutter.github_org}}/{{cookiecutter.__package_slug}}.celery`
{%- endif %}

### Image Tags

Multiple tags are created for each build:

- **Branch builds**: `main`, `develop`, etc.
- **PR builds**: `pr-123`
- **Version builds**: `v1.2.3`, `v1.2`, `v1`, `latest`

### Multi-Architecture Support

Images are built for multiple architectures:

- `linux/amd64` - Intel/AMD processors
- `linux/arm64` - ARM processors (Apple Silicon, ARM servers)

Use the same image tag across architectures:

```bash
# Automatically pulls correct architecture
docker pull ghcr.io/{{cookiecutter.github_org}}/{{cookiecutter.__package_slug}}.www:latest
```

### Pulling Images

```bash
# Pull latest development version
docker pull ghcr.io/{{cookiecutter.github_org}}/{{cookiecutter.__package_slug}}.www:main

# Pull specific version
docker pull ghcr.io/{{cookiecutter.github_org}}/{{cookiecutter.__package_slug}}.www:v1.2.3

# Use in docker-compose
services:
  www:
    image: ghcr.io/{{cookiecutter.github_org}}/{{cookiecutter.__package_slug}}.www:v1.2.3
```

### Image Visibility

By default, images are public. To make them private:

1. Go to the package page on GitHub
2. Click "Package settings"
3. Change visibility to "Private"
{%- endif %}

## Customizing Workflows

### Adding a New Workflow

Create `.github/workflows/my-workflow.yaml`:

```yaml
name: My Custom Workflow

on:
  push:
  pull_request:

jobs:
  my-job:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - uses: actions/setup-python@v6
        with:
          python-version-file: .python-version

      - name: Install Dependencies
        run: make install

      - name: Run Custom Command
        run: echo "Hello, World!"
```

### Modifying Existing Workflows

Edit workflow files in `.github/workflows/`:

```yaml
# Add a new Python version to test matrix
strategy:
  matrix:
    version: ["3.10", "3.11", "3.12", "3.15"]  # Add 3.15
```

### Conditional Workflow Execution

Run jobs only on specific branches:

```yaml
jobs:
  deploy:
    if: {% raw %}github.ref == 'refs/heads/main'{% endraw %}
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: echo "Deploying..."
```

### Workflow Dependencies

Make jobs depend on others:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Run Tests
        run: make test

  deploy:
    needs: test  # Only runs if 'test' succeeds
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: echo "Deploying..."
```

## Debugging Failed Workflows

### View Workflow Logs

1. Go to the Actions tab on GitHub
2. Click on the failed workflow run
3. Click on the failed job
4. Expand the failed step to see detailed logs

### Re-run Failed Jobs

Click "Re-run jobs" → "Re-run failed jobs" to retry without new commits

### Debug Locally

Run the same commands locally:

```bash
# Run what pytest workflow runs
make install
make pytest

# Run what ruff workflow runs
make install
make ruff_check

# Run all checks
make tests
```

### Enable Debug Logging

Add `ACTIONS_STEP_DEBUG` secret with value `true` for verbose logging.

### Common Issues

**Tests pass locally but fail in CI:**

- Check Python version differences
- Verify environment variables
- Check for missing dependencies
- Review test isolation

{%- if cookiecutter.include_sqlalchemy == "y" %}

**Alembic check fails:**

- Run `make create_migration MESSAGE="description"` locally
- Commit and push the new migration file
{%- endif %}

**Docker build fails:**

- Check Dockerfile syntax
- Verify base image exists
- Review build logs for missing dependencies

## Dependabot Configuration

The project includes Dependabot for automated dependency updates.

### Configuration

`.github/dependabot.yml`:

```yaml
version: 2

updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### What Dependabot Does

- **Checks weekly** for GitHub Actions updates
- **Creates PRs** automatically for outdated actions
- **Runs tests** on dependency update PRs
- **Provides changelogs** and release notes in PR descriptions

### Managing Dependabot PRs

1. **Review the PR**: Check changelog and breaking changes
2. **Run tests**: CI automatically runs on Dependabot PRs
3. **Merge if green**: Merge when all checks pass
4. **Close if not needed**: Close if update isn't desired

## Workflow Performance

### Optimization Tips

1. **Cache dependencies**:

   ```yaml
   - uses: actions/cache@v4
     with:
       path: ~/.cache/pip
       key: {% raw %}${{ runner.os }}-pip-${{ hashFiles('pyproject.toml') }}{% endraw %}
   ```

2. **Use matrix builds** for parallel testing:

   ```yaml
   strategy:
     matrix:
       version: ["3.10", "3.11", "3.12"]
   ```

3. **Fail fast** to save time on obvious failures:

   ```yaml
   strategy:
     fail-fast: true
   ```

4. **Skip workflows** on documentation-only changes:

   ```yaml
   on:
     push:
       paths-ignore:
         - '**.md'
         - 'docs/**'
   ```

## Best Practices

1. **Keep workflows simple**: One clear purpose per workflow

2. **Use make commands**: Workflows run `make` targets for consistency with local development

3. **Test workflow changes**: Test in a branch before merging workflow changes

4. **Pin action versions**: Use specific versions for actions (e.g., `@v5` not `@latest`)

5. **Use secrets for sensitive data**: Never hardcode credentials

6. **Document custom workflows**: Add comments explaining complex logic

7. **Monitor workflow usage**: Check Actions tab regularly for failures

8. **Keep dependencies updated**: Review and merge Dependabot PRs promptly

## Workflow Costs and Limits

GitHub Actions has usage limits:

- **Public repositories**: Unlimited minutes (with some restrictions)
- **Private repositories**: 2,000 minutes/month free, then paid
- **Storage**: 500 MB free, artifacts expire after 90 days

To optimize:

- Use caching to reduce build times
- Clean up old artifacts
- Use `concurrency` to cancel outdated runs

```yaml
concurrency:
  group: {% raw %}${{ github.workflow }}-${{ github.ref }}{% endraw %}
  cancel-in-progress: true
```

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
