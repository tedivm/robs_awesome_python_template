# Documentation

This project maintains comprehensive developer documentation to help developers understand, extend, and contribute to the codebase. All documentation follows consistent standards and best practices to ensure quality, accuracy, and usefulness.

## Overview

Documentation is organized in the `docs/dev/` directory, with each major feature or topic having its own dedicated file. Documentation is written in Markdown and follows consistent structures appropriate to the content type.

## Documentation Standards

All documentation in this project follows these standards to ensure consistency and quality:

### 1. Structure and Organization

**Feature Documentation Structure**: Documentation for features and tools should follow this standard structure:

```markdown
# Feature Name

Brief introduction explaining what the feature is and what library/tool it uses.

## Overview

High-level explanation of the feature's purpose and capabilities.

## Configuration

How to configure the feature (environment variables, settings, etc.).

## Usage

How to use the feature with practical examples.

## Testing

How to test code that uses this feature.

## Best Practices

Recommendations and patterns for using the feature effectively.

## Development vs Production

Differences between development and production configurations.

## References

Links to official documentation and related resources.
```

**Other Documentation Types**: Tutorials, guides, and conceptual documentation may follow different structures appropriate to their purpose. The key is consistency within each documentation type.

**Optional Sections** (include when relevant):

- Common Patterns
- Troubleshooting
- Advanced Usage
- Performance Considerations
- Security Considerations

### 2. Code Examples

**Real, Working Code**: All code examples must be:

- Taken from or compatible with the actual project structure
- Fully functional and runnable
- Using actual project imports and modules
- Verified against the implementation

**Bad Example** (generic, fictional):

```python
# Don't do this - generic example not specific to the project
from some_library import cache

@cache.cached()
def get_data():
    return "data"
```

**Good Example** (project-specific):

```python
# Do this - uses actual project structure
from {{cookiecutter.__package_slug}}.services.cache import get_cached, set_cached

async def get_user_profile(user_id: int):
    """Get user profile with caching."""
    # Check cache first
    cached_profile = await get_cached(f"user:{user_id}", alias="persistent")
    if cached_profile:
        return cached_profile

    # Fetch from database
    profile = await fetch_profile_from_db(user_id)

    # Cache for 1 hour
    await set_cached(f"user:{user_id}", profile, ttl=3600, alias="persistent")
    return profile
```

### 3. Testing Examples

**Use Actual Fixtures**: Testing examples must use the project's actual test fixtures defined in `conftest.py`:

- `db_session` - Database session fixture
- `fastapi_client` - FastAPI test client fixture
- `runner` - Typer CLI test runner fixture

**Bad Example** (fictional fixtures):

```python
# Don't do this - uses made-up fixtures
def test_something(mock_client):
    response = mock_client.get("/endpoint")
    assert response.status_code == 200
```

**Good Example** (actual fixtures):

```python
# Do this - uses actual project fixtures
def test_api_endpoint(fastapi_client):
    """Test the API endpoint using the actual test client fixture."""
    response = fastapi_client.get("/users/1")
    assert response.status_code == 200
    assert "name" in response.json()
```

#### Completeness

Documentation should cover the feature comprehensively:

- **Complete Lifecycle**: From setup to advanced usage
- **Error Handling**: What can go wrong and how to fix it
- **Real Examples**: Working code from the actual project
- **Depth**: Provide enough detail for both basic usage and advanced scenarios

### 5. Accuracy and Verification

**Verify Everything**: Before documenting:

- Run all code examples to ensure they work
- Check that imports and module paths are correct
- Verify environment variables and settings
- Test commands and makefile targets
- Confirm library versions and behavior

**Keep Updated**: When code changes:

- Update affected documentation
- Verify examples still work
- Update version-specific information
- Check for deprecated features

### 6. Contextual Teaching

**Teach in Context**: Documentation should:

- Explain **how to use features within this project's structure**
- Show **actual patterns from the project**
- Demonstrate **integration with other features**
- Reference **actual project files and modules**

**Avoid Generic Tutorials**: Don't just copy library documentation. Instead:

- Show how the library is configured **in this project**
- Demonstrate patterns **specific to this project**
- Explain decisions and conventions **used in this codebase**
- Link to official docs for additional details

### 7. Development-Focused

**Target Audience**: Documentation is written for developers who:

- Are building and maintaining this application
- Need to understand how features work together
- Want to extend or customize functionality
- Are contributing to this project

**Practical Focus**: Emphasize:

- Common development tasks
- Real-world usage patterns
- Integration points between features
- Testing strategies
- Debugging techniques

## Writing New Documentation

When creating new documentation or expanding existing docs:

### 1. Research Phase

Before writing:

- Review the feature's implementation in the codebase
- Test the feature with various configurations
- Examine how it's used in the project
- Check official library documentation
- Look at test files for usage patterns

### 2. Outline Phase

Create a structure:

```markdown
# Feature Name
## Overview
## Configuration
## Basic Usage
## Common Patterns
## Testing
## Best Practices
## References
```

### 3. Writing Phase

Follow these guidelines:

**Start with Introduction**:

```markdown
# Feature Name

This project uses [Library Name](url) for [purpose], providing [key capabilities].
```

**Configuration Section**:

- List all environment variables
- Show default values
- Explain what each setting controls
- Group related settings together

**Usage Section**:

- Start with simplest example
- Add complexity gradually
- Show multiple approaches
- Include comments explaining code

**Testing Section**:

- Use actual project fixtures
- Show test structure and patterns
- Demonstrate assertions
- Cover async testing when applicable

**Best Practices Section**:

Numbered list of recommendations:

```markdown
1. **Practice Name**: Brief explanation

   ```python
   # Good
   example_code()

   # Bad
   wrong_code()
   ```

```

### 4. Review Phase

Before finalizing:

- [ ] Run all code examples
- [ ] Verify all imports work
- [ ] Test all commands and makefile targets
- [ ] Check links to external resources
- [ ] Ensure consistent formatting
- [ ] Verify it matches the standard structure
- [ ] Get feedback from another developer

## Documentation Maintenance

### Regular Updates

Documentation should be updated when:

- New features are added
- APIs change
- Configuration options change
- Dependencies are updated
- Best practices evolve

### Version Considerations

When documenting version-specific behavior:

```markdown
**Note**: This feature requires Python 3.11+
```

### Deprecation Notices

When features are deprecated:

```markdown
**Deprecated**: This approach is deprecated in favor of [new approach].
See [link to new docs] for the recommended pattern.
```

## Common Documentation Patterns

### Command Examples

Show commands with explanations:

```markdown
```bash
# Run tests with coverage
make pytest

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

```

### Configuration Tables

Use lists for configuration options:

```markdown
- **SETTING_NAME**: Description (default: `value`)
  - Additional details or notes
```

### Code Annotations

Add comments to explain code:

```python
async def example_function():
    """Docstring explaining the function."""
    # Step 1: Fetch data
    data = await fetch_data()

    # Step 2: Process the result
    processed = process(data)

    # Step 3: Return formatted output
    return format_output(processed)
```



## Testing Documentation

Documentation itself should be tested:

### Automated Checks

The project includes checks for:

- Broken links (internal and external)
- Code syntax in examples
- Markdown formatting

### Manual Testing

When updating documentation:

1. Follow the documentation steps yourself
2. Run all example commands
3. Verify code examples work
4. Check that links are valid

## Documentation Tools

### Markdown Linting

The project uses markdownlint for consistency:

```bash
# Check markdown formatting
make lint_markdown
```

### Schema Documentation

Database schema is auto-generated:

```bash
# Update schema documentation
make document_schema
```

This uses [Paracelsus](https://github.com/tedivm/paracelsus) to inject schema information into database.md.

### Link Checking

Verify all links in documentation:

```bash
# Check for broken links
make check_links
```

## Best Practices

1. **Write as You Code**: Document features as you implement them, not after

2. **Test Your Examples**: Never publish documentation with untested code examples

3. **Use Actual Imports**: Always use the project's actual module structure in examples

4. **Show, Don't Tell**: Prefer code examples over lengthy explanations

5. **Link to Official Docs**: Reference official library documentation for detailed API information

6. **Keep It Current**: Update documentation when you change code

7. **Be Specific**: Use concrete examples from the project, not generic tutorials

8. **Consider Your Audience**: Write for developers working on this project, not library beginners

9. **Explain Decisions**: Document why certain patterns or configurations are used

10. **Maintain Consistency**: Follow the established structure and style

## Resources

- [Markdown Guide](https://www.markdownguide.org/)
- [Write the Docs](https://www.writethedocs.org/)
- [Google Developer Documentation Style Guide](https://developers.google.com/style)
- [Divio Documentation System](https://documentation.divio.com/)

## Contributing to Documentation

When contributing documentation improvements:

1. Review existing documentation for style and structure
2. Follow the standards outlined in this document
3. Test all code examples in the project
4. Use actual project fixtures and patterns
5. Get feedback through pull request review
6. Update this documentation.md if adding new standards

## Meta-Documentation

This file itself follows the standards it describes:

- Consistent structure with clear sections
- Practical examples of documentation patterns
- Best practices with numbered lists
- References to external resources
- Focus on project-specific context
- Teaching through demonstration

By following these standards, we ensure that all project documentation is:

- **Accurate**: Reflects actual implementation
- **Useful**: Helps developers accomplish tasks
- **Consistent**: Follows predictable patterns
- **Maintainable**: Easy to update as code evolves
- **Comprehensive**: Covers common use cases and edge cases

Good documentation is a force multiplier that enables developers to work effectively and confidently.
