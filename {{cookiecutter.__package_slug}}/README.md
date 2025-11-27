# {{ cookiecutter.package_name }}

{{cookiecutter.short_description}}

{%- if cookiecutter.publish_to_pypi == "y" %}

## Installation

```bash
pip install {{ cookiecutter.package_name }}
```

{%- endif %}


{%- if cookiecutter.include_cli == "y" %}

## CLI

```bash
{{ cookiecutter.__package_slug }} --help
```

{%- endif %}

## Developer Documentation

Comprehensive developer documentation is available in [`docs/dev/`](./docs/dev/) covering testing, configuration, deployment, and all project features.

### Quick Start for Developers

```bash
# Install development environment
make install
{%- if cookiecutter.include_docker == "y" %}

# Start services with Docker
docker compose up -d
{%- endif %}

# Run tests
make tests

# Auto-fix formatting
make chores
```

See the [developer documentation](./docs/dev/README.md) for complete guides and reference.
