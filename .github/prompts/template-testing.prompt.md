---
description: "Comprehensive testing of the cookiecutter template across all configurations."
---

# Template Testing Prompt

Please perform comprehensive testing of the cookiecutter template to ensure all configurations generate working projects with passing tests, type checking, and linting.

## Task Requirements:

### 1. Standard Test Configurations

Test ALL three standard configurations located in the `tests/` directory:

- **Full configuration** (`tests/full.yaml`): All features enabled (FastAPI, Celery, QuasiQueue, Database, Caching, Docker)
- **Library configuration** (`tests/library.yaml`): Minimal setup for Python library development
- **Bare configuration** (`tests/bare.yaml`): Basic project with no optional features

### 2. Testing Workflow

For EACH configuration, perform these steps:

#### Step 1: Generate Project

```bash
cd /Users/tedivm/Repositories/tedivm/robs_awesome_python_template
rm -rf workspaces/<config_name>
cookiecutter --config-file tests/<config_name>.yaml --no-input --output-dir workspaces .
cd workspaces/<config_name>
```

#### Step 2: Run Test Suite

Run the key validation checks:

```bash
make pytest      # Run all tests with coverage
make mypy_check  # Type checking
make ruff_check  # Linting
```

Note: Formatting issues (dapperdata, tomlsort, paracelsus) can be auto-fixed with `make chores` and are not critical for validation.

#### Step 3: Verify Results

Check that:

- ✅ All tests pass (exit code 0)
- ✅ Test coverage meets expectations (typically 90%+ for full/library, 100% for bare)
- ✅ No mypy type errors
- ✅ No ruff linting errors
- ✅ Code formatting is correct

### 3. Context-Specific Testing

**IMPORTANT:** In addition to the three standard configurations, create and test additional custom configurations relevant to your current work session.

For example:

- If you modified caching functionality, test a config with caching enabled and one with it disabled
- If you updated Docker configurations, test with and without Docker components
- If you modified CLI functionality, test with and without optional CLI features
- If you modify a component with hooks into a lot of other systems, create multiple configurations to validate those changes

#### Creating Custom Test Configurations

Create temporary YAML config files in the `workspaces/` directory (these won't be committed):

```yaml
# Example: workspaces/custom_test.yaml
default_context:
  project_name: "Custom Test"
  project_slug: "custom_test"
  package_name: "custom_test"
  include_fastapi: "y"
  include_celery: "n"
  include_database: "y"
  include_caching: "y"
  # ... other settings as needed
```

Then test with:

```bash
cookiecutter --config-file workspaces/custom_test.yaml --no-input --output-dir workspaces .
```

### 4. Expected Test Results

Standard configurations should produce these results:

#### Bare Configuration

- **Tests**: ~11 tests
- **Coverage**: 100%
- **Files tested**: Core settings and configuration

#### Library Configuration

- **Tests**: ~26 tests
- **Coverage**: ~93%
- **Files tested**: CLI, settings, basic project structure
- **Note**: CLI should have version and hello commands

#### Full Configuration

- **Tests**: ~147 tests
- **Coverage**: ~94%
- **Files tested**: All services (cache, db, jinja), celery, CLI, QuasiQueue, FastAPI, settings
- **Note**: Most comprehensive test suite with all features

### 5. Common Issues and Troubleshooting

#### Issue: Jinja2 Template Errors

- **Cause**: Raw Jinja2 code in documentation or examples
- **Solution**: Ensure all Jinja2 examples in markdown files are wrapped in `{% raw %}...{% endraw %}`

#### Issue: Mypy Type Errors

- **Cause**: Missing type annotations or untyped library imports
- **Solution**: Check pyproject.toml has strict mypy settings enabled; use `# type: ignore` for untyped third-party libraries as a last resort only

#### Issue: CLI Tests Failing

- **Cause**: Typer single-command behavior or missing commands
- **Solution**: Ensure CLI always has at least 2 commands (version + hello minimum)

#### Issue: Import Errors

- **Cause**: Optional dependencies not properly handled
- **Solution**: Check that conditional imports use try/except blocks or are properly guarded

### 6. Reporting Results

After testing, provide a summary that includes:

1. **Configuration Results**: For each tested configuration

   - Configuration name
   - Number of tests run
   - Number of tests passed/failed
   - Code coverage percentage
   - Any errors or warnings

2. **Test Output Analysis**: Key findings from test execution

   - Any deprecation warnings
   - Performance issues
   - Coverage gaps in important modules

3. **Validation Status**: Overall health check
   - ✅ All standard configurations passing
   - ✅ Context-specific configurations passing
   - ✅ Type checking clean (mypy)
   - ✅ Linting clean (ruff)
   - ✅ Formatting correct (black)

### 7. Performance Considerations

- Run tests in sequence, not parallel (to avoid resource conflicts)
- Clean up workspace directories between runs to ensure fresh state
- Virtual environments can be reused within a configuration but should be recreated between different configurations

### 8. Template Context Awareness

Remember that this is a **cookiecutter template project**, which means:

- The actual template files are in `{{cookiecutter.__package_slug}}/`
- Test configurations are in `tests/*.yaml`
- Generated projects appear in `workspaces/`
- Many files contain Jinja2 templating syntax that looks like broken Python/YAML
- The `hooks/post_gen_project.py` script removes unnecessary files based on configuration

### 9. Success Criteria

Testing is considered successful when:

- ✅ All three standard configurations generate working projects
- ✅ All test suites pass with high coverage (90%+)
- ✅ No type checking errors (mypy clean)
- ✅ No linting errors (ruff clean)
- ✅ All formatting is correct (black clean)
- ✅ Any context-specific configurations relevant to recent changes also pass
- ✅ Exit codes are 0 for all test runs
- ✅ No warnings or errors in test output

## Implementation Approach:

1. **Prepare**: Understand what changes were made in the current session
2. **Plan**: Identify which configurations are most relevant to test
3. **Execute**: Run standard configurations (bare, library, full) sequentially
4. **Validate**: Create and test custom configurations for specific scenarios
5. **Report**: Provide clear summary of all test results
6. **Iterate**: If any tests fail, investigate and fix before proceeding

Remember: Testing is not just about running commands—it's about validating that the template produces high-quality, production-ready Python projects across all supported configurations.
