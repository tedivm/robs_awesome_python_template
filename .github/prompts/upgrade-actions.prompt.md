---
description: "Upgrade action versions in workflows of the template."
---

# GitHub Actions Version Upgrade Prompt

Please update all GitHub workflow files in the template directory (`{{cookiecutter.__package_slug}}/.github/workflows/`) to use the latest action versions while maintaining major version references and preserving all Jinja templating.

## Task Requirements:

### 1. File Location

- Target directory: `{{cookiecutter.__package_slug}}/.github/workflows/`
- Update ALL `.yaml` workflow files in this directory
- These are Jinja template files, so YAML formatting may appear broken due to template syntax - this is expected and should be preserved

### 2. Actions to Update

- **First, discover all GitHub Actions used** by reading through all workflow files in the target directory
- **Research each action's latest version** by checking their respective GitHub releases pages
- **Categorize actions appropriately**:
  - Core GitHub actions (actions/\*)
  - Docker actions (docker/\*)
  - PyPI/Python actions (pypa/\*)
  - Third-party actions (other organizations)
- **Apply appropriate update strategies** based on action type and current version patterns

### 3. Version Format Rules

- **Use MAJOR versions only** (e.g., `v5`, `v6`, not `v5.2.1` or `v6.18.0`)
- Major version tags automatically receive compatible updates
- Exception: `pypa/gh-action-pypi-publish@release/v1` should stay as-is

### 4. Research Method

- Look up latest versions by fetching GitHub releases pages
- Infer GitHub URLs from action names (e.g., `actions/checkout` → `https://github.com/actions/checkout/releases`)
- Use the web to find the most recent stable major version
- Don't update to pre-release or beta versions

### 5. Template Preservation

**CRITICAL:** Preserve ALL existing Jinja template syntax:

- `{% raw %}${{ github.actor }}{% endraw %}`
- `{% raw %}${{ secrets.GITHUB_TOKEN }}{% endraw %}`
- `{% raw %}${{ matrix.version }}{% endraw %}`
- Cookiecutter variables like `cookiecutter.include_fastapi`
- Conditional blocks: `{%- if cookiecutter.include_celery == "y" %}`
- Template comments and whitespace

### 6. File Discovery

- **Discover all workflow files** by listing all `.yaml` files in the target directory
- **Don't assume file names** - read the directory contents to find all workflow files that need updating

### 7. Verification Steps

After updating:

1. Confirm all action versions are updated to latest major versions
2. Verify Jinja templating is intact
3. Check that YAML structure is preserved (even if it looks broken due to templates)

### 8. Example Updates

```yaml
# Before:
- uses: actions/checkout@v4
- uses: actions/setup-python@v5
- uses: docker/setup-qemu-action@v3.2.0

# After:
- uses: actions/checkout@v5
- uses: actions/setup-python@v6
- uses: docker/setup-qemu-action@v3
```

## Implementation Approach:

1. **Discover**: List all workflow files and identify all GitHub Actions used
2. **Research**: Look up current latest versions for each discovered action
3. **Plan**: Create a mapping of old version → new version
4. **Update**: Use precise string replacement to update each action reference
5. **Verify**: Check a few files to ensure changes are correct and templates preserved

Remember: This is a cookiecutter template, so the YAML may appear malformed due to Jinja syntax, but this is intentional and must be preserved.
