# PyPI Publishing

This project is configured to build and publish Python packages to the Python Package Index (PyPI) using automated GitHub Actions workflows. The publishing process uses OpenID Connect (OIDC) for secure, token-free authentication.

## Overview

The PyPI workflow automatically:

- Builds package distributions on every push and pull request
- Validates the package can be built successfully
- Publishes to PyPI when version tags are pushed (if enabled)
- Uses trusted publishing via OIDC (no API tokens needed)

## Package Configuration

### Version Management

This project uses `setuptools_scm` for automatic versioning based on git tags:

**Development Versions**:

- Versions are automatically generated from git history
- Format: `0.0.0.devN+gHASH` (e.g., `0.2.3.dev42+g1234abc`)
- Includes commit count and hash

**Release Versions**:

- Determined by git tags
- Must follow semantic versioning: `vMAJOR.MINOR.PATCH` (e.g., `v1.2.3`)
- Tag format triggers PyPI publishing

**Configuration** (`pyproject.toml`):

```toml
[tool.setuptools_scm]
fallback_version = "0.0.0-dev"
write_to = "{{cookiecutter.__package_slug}}/_version.py"
```

The version is written to `_version.py` and imported by the package.

### Package Metadata

Key metadata in `pyproject.toml`:

```toml
[project]
name = "{{cookiecutter.__package_slug}}"
description = "{{cookiecutter.short_description}}"
authors = [{"name" = "{{cookiecutter.author_name}}"}]
readme = {file = "README.md", content-type = "text/markdown"}
license = {"file" = "LICENSE"}
dynamic = ["version"]
```

**Important Fields**:

- **name**: Package name on PyPI (must be unique)
- **description**: Short description shown in search results
- **readme**: Long description shown on PyPI page
- **license**: License information
- **dynamic**: Version is determined by setuptools_scm

## Building Packages

### Local Build

Build packages locally for testing:

```bash
# Build source distribution and wheel
make build

# Output in dist/ directory
ls dist/
# {{cookiecutter.__package_slug}}-1.2.3.tar.gz
# {{cookiecutter.__package_slug}}-1.2.3-py3-none-any.whl
```

**Build Artifacts**:

- **Source Distribution** (`.tar.gz`): Complete source code package
- **Wheel** (`.whl`): Pre-built binary package (faster to install)

### Verify Build

Test installation from the built package:

```bash
# Create clean virtual environment
python -m venv test-env
source test-env/bin/activate

# Install from wheel
pip install dist/{{cookiecutter.__package_slug}}-*.whl

# Verify installation
python -c "import {{cookiecutter.__package_slug}}; print({{cookiecutter.__package_slug}}.__version__)"

# Clean up
deactivate
rm -rf test-env
```

### Check Package

Validate package metadata and contents:

```bash
# Install twine for checking
pip install twine

# Check package
twine check dist/*
```

This verifies:

- README renders correctly on PyPI
- Metadata is valid
- Package structure is correct

## GitHub Actions Workflow

### Workflow Trigger

The PyPI workflow (`.github/workflows/pypi.yaml`) runs on:

**Every Push and PR**:

- Builds the package
- Validates build succeeds
- Does not publish

**Version Tags**:

- Builds the package
- Publishes to PyPI (if `PUBLISH_TO_PYPI=true`)
- Only on tags matching `v[0-9]+.[0-9]+.[0-9]+`

### Workflow Configuration

```yaml
name: PyPI

on:
  push:
    branches:
      - "**"
    tags:
      - "v[0-9]+.[0-9]+.[0-9]+"
  pull_request:

env:
  PUBLISH_TO_PYPI: true  # Set during project generation

jobs:
  pypi:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # Required for OIDC
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0    # Full history for setuptools_scm
          fetch-tags: true  # Ensure tags are fetched

      - uses: actions/setup-python@v6
        with:
          python-version-file: .python-version

      - name: Install Dependencies
        run: make install

      - name: Build Wheel
        run: make build

      - name: Publish package
        if: env.PUBLISH_TO_PYPI == 'true' && github.event_name == 'push' && startsWith(github.ref, 'refs/tags')
        uses: pypa/gh-action-pypi-publish@release/v1
```

**Key Points**:

- **fetch-depth: 0**: Fetches complete git history (required for version calculation)
- **fetch-tags: true**: Ensures tags are available
- **permissions.id-token: write**: Enables OIDC authentication
- **Conditional publish**: Only publishes on tag pushes when enabled

## OIDC Trusted Publishing

### What is OIDC Publishing?

OpenID Connect (OIDC) publishing is a secure, token-free way to publish packages to PyPI:

**Benefits**:

- No API tokens to manage or rotate
- No secrets to store in GitHub
- Automatic authentication via GitHub's identity
- Reduced security risk (no leaked tokens)
- Scoped to specific repository and workflow

**How It Works**:

1. GitHub Actions generates a temporary OIDC token
2. Token proves the workflow's identity to PyPI
3. PyPI validates the token matches configured publisher
4. Package is published if validation succeeds

### Setting Up OIDC on PyPI

**Prerequisites**:

- PyPI account with verified email
- Repository with PyPI workflow configured
- Package name available on PyPI

#### Step 1: Create PyPI Account

1. Go to [https://pypi.org/account/register/](https://pypi.org/account/register/)
2. Create account and verify email
3. Enable two-factor authentication (recommended)

#### Step 2: Register Package Name

**Option A: Reserve Name (Recommended)**

1. Go to [https://pypi.org/manage/account/publishing/](https://pypi.org/manage/account/publishing/)
2. Click "Add a new pending publisher"
3. Fill in the form:
   - **PyPI Project Name**: `{{cookiecutter.__package_slug}}`
   - **Owner**: Your GitHub username or organization
   - **Repository name**: Your repository name
   - **Workflow name**: `pypi.yaml`
   - **Environment name**: Leave blank (not used)
4. Click "Add"

**Option B: Publish First Version Manually**

If you prefer to publish the first version manually:

```bash
# Build package
make build

# Install twine
pip install twine

# Upload to PyPI (will prompt for credentials)
twine upload dist/*
```

Then configure OIDC for future releases.

#### Step 3: Configure Trusted Publisher

If you published manually first:

1. Go to your project page: `https://pypi.org/project/{{cookiecutter.__package_slug}}/`
2. Click "Manage" → "Publishing"
3. Scroll to "Trusted Publishers"
4. Click "Add a new publisher"
5. Select "GitHub Actions"
6. Fill in:
   - **Owner**: Your GitHub username/org
   - **Repository name**: Your repository name
   - **Workflow name**: `pypi.yaml`
   - **Environment name**: Leave blank
7. Click "Add"

#### Step 4: Verify Configuration

Check the configuration:

```yaml
# Should match your PyPI trusted publisher settings
Owner: your-username
Repository: your-repo-name
Workflow: pypi.yaml
Environment: (none)
```

## Publishing a Release

### Step 1: Prepare Release

```bash
# Ensure you're on main branch
git checkout main
git pull

# Ensure all tests pass
make tests

# Verify build works
make build

# Check package metadata
pip install twine
twine check dist/*
```

### Step 2: Create Version Tag

Choose semantic version number:

- **Major** (v2.0.0): Breaking changes
- **Minor** (v1.3.0): New features, backward compatible
- **Patch** (v1.2.4): Bug fixes, backward compatible

```bash
# Create annotated tag
git tag -a v1.2.3 -m "Release version 1.2.3"

# View tag details
git show v1.2.3

# Push tag to GitHub
git push origin v1.2.3
```

**Important**: The tag must match the pattern `v[0-9]+.[0-9]+.[0-9]+` exactly.

### Step 3: Monitor Workflow

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Find the "PyPI" workflow run
4. Watch the build and publish steps

**Expected Output**:

```
✓ Checkout code
✓ Setup Python
✓ Install Dependencies
✓ Build Wheel
✓ Publish package to PyPI
```

### Step 4: Verify Publication

Check the package on PyPI:

```bash
# View on PyPI
open https://pypi.org/project/{{cookiecutter.__package_slug}}/

# Install from PyPI
pip install {{cookiecutter.__package_slug}}

# Verify version
python -c "import {{cookiecutter.__package_slug}}; print({{cookiecutter.__package_slug}}.__version__)"
```

## Release Checklist

Before tagging a release:

- [ ] All tests pass (`make tests`)
- [ ] Changelog/release notes updated
- [ ] Version number decided (semantic versioning)
- [ ] README is current
- [ ] Documentation is up-to-date
- [ ] Breaking changes documented (if major version)
- [ ] Dependencies are up-to-date
- [ ] Build succeeds locally (`make build`)
- [ ] Package check passes (`twine check dist/*`)
- [ ] OIDC trusted publisher configured on PyPI

After tagging:

- [ ] GitHub Actions workflow succeeds
- [ ] Package appears on PyPI
- [ ] Installation from PyPI works
- [ ] Create GitHub Release with notes
- [ ] Announce release (if appropriate)

## Troubleshooting

### Build Fails: "No module named '_version'"

**Problem**: Version file not generated.

**Solution**:

```bash
# Ensure git tags are present
git fetch --tags

# Reinstall with setuptools_scm
pip install -e .

# Check version file exists
ls {{cookiecutter.__package_slug}}/_version.py
```

### Publish Fails: "Not a valid publisher"

**Problem**: OIDC trusted publisher not configured correctly.

**Solution**:

1. Verify configuration on PyPI matches workflow
2. Check repository owner/name spelling
3. Ensure workflow name is exactly `pypi.yaml`
4. Verify tag format: `v1.2.3` (not `1.2.3` or `version-1.2.3`)

### Publish Fails: "Package already exists"

**Problem**: Version already published to PyPI.

**Solution**:

PyPI does not allow replacing versions. You must:

```bash
# Delete the tag
git tag -d v1.2.3
git push origin :refs/tags/v1.2.3

# Create new patch version
git tag -a v1.2.4 -m "Release version 1.2.4"
git push origin v1.2.4
```

### Version is "0.0.0-dev"

**Problem**: Git tags not available or setuptools_scm not configured.

**Solution**:

```bash
# Fetch tags
git fetch --tags

# Create initial tag if none exist
git tag v0.1.0
git push origin v0.1.0

# Reinstall package
pip install -e .
```

### Workflow Doesn't Trigger

**Problem**: Tag format doesn't match workflow pattern.

**Solution**:

Ensure tag format is exactly `vMAJOR.MINOR.PATCH`:

```bash
# ✓ Correct formats
v1.0.0
v2.3.4
v10.20.30

# ✗ Incorrect formats
1.0.0        # Missing 'v' prefix
v1.0         # Missing patch version
v1.0.0-beta  # Has suffix
version1.0.0 # Wrong prefix
```

### Permission Denied on PyPI

**Problem**: OIDC not configured or wrong repository.

**Solution**:

1. Verify you're on the correct repository
2. Check OIDC configuration on PyPI
3. Ensure `permissions.id-token: write` in workflow
4. Verify PyPI account has access to package name

## Security Best Practices

1. **Use OIDC**: Avoid storing PyPI tokens as GitHub secrets

2. **Protected Tags**: Configure branch protection for tags:
   - Settings → Branches → Add tag protection rule
   - Pattern: `v*`
   - Prevents unauthorized releases

3. **Required Reviews**: Require PR reviews before merging to main

4. **Two-Factor Auth**: Enable 2FA on PyPI account

5. **Monitor Releases**: Watch for unexpected package publications

6. **Verify Checksums**: Check package integrity after publishing

7. **Audit Logs**: Review PyPI and GitHub audit logs regularly

## Version Strategy

### Semantic Versioning

Follow [Semantic Versioning 2.0.0](https://semver.org/):

**MAJOR.MINOR.PATCH** (e.g., 2.3.1)

- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible new features
- **PATCH**: Backward-compatible bug fixes

### Pre-release Versions

For pre-releases, use suffixes:

```bash
# Alpha release
git tag v1.0.0-alpha.1

# Beta release
git tag v1.0.0-beta.1

# Release candidate
git tag v1.0.0-rc.1
```

**Note**: Pre-release tags don't match the workflow pattern and won't auto-publish. This is intentional for safety.

### Development Versions

Between releases, setuptools_scm generates dev versions:

```python
# After v1.2.0, before next tag
"1.2.1.dev5+g1234abc"
# 1.2.1: Next version
# dev5: 5 commits since tag
# g1234abc: Git commit hash
```

## Manual Publishing

If needed, you can publish manually:

```bash
# Build package
make build

# Install twine
pip install twine

# Upload to PyPI
twine upload dist/*

# Or upload to Test PyPI first
twine upload --repository testpypi dist/*
```

**Test PyPI**:

- URL: [https://test.pypi.org/](https://test.pypi.org/)
- Use for testing before production
- Separate account from production PyPI

## Continuous Delivery

This setup enables continuous delivery:

1. **Develop**: Make changes on feature branches
2. **Test**: PR builds verify package builds successfully
3. **Merge**: Merge to main after review
4. **Release**: Tag commit to trigger publication
5. **Deploy**: Package automatically published to PyPI

**Benefits**:

- Fast releases (tag and done)
- Consistent build process
- No manual upload steps
- Built-in verification

## References

- [PyPI Trusted Publishers Guide](https://docs.pypi.org/trusted-publishers/)
- [GitHub Actions OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [Semantic Versioning](https://semver.org/)
- [setuptools_scm Documentation](https://setuptools-scm.readthedocs.io/)
- [Python Packaging Guide](https://packaging.python.org/)
- [twine Documentation](https://twine.readthedocs.io/)

## See Also

- [GitHub Actions](./github.md) - Complete CI/CD workflow documentation
- [Dependencies](./dependencies.md) - Managing project dependencies
- [Makefile](./makefile.md) - Build commands and automation
