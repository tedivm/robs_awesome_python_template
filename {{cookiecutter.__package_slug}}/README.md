# {{ cookiecutter.package_name }}


{%- if cookiecutter.publish_to_pypi == "y" %}

## Installation

```bash
pip install {{ cookiecutter.package_name }}
```

{%- endif %}


{%- if cookiecutter.include_cli == "y" %}

## CLI

```bash
{{ cookiecutter.__package_cli }} --help
```

{%- endif %}
