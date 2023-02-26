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
