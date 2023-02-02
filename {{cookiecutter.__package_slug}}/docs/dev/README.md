# Developer Readme

{%- if cookiecutter.include_fastapi == "y" %}

1. [Rest API](./api.md)
{%- endif %}
{%- if cookiecutter.include_dogpile == "y" %}
1. [Caching](./cache.md)
{%- endif %}
{%- if cookiecutter.include_celery == "y" %}
1. [Celery](./celery.md)
{%- endif %}
{%- if cookiecutter.include_cli == "y" %}
1. [CLI](./cli.md)
{%- endif %}
{%- if cookiecutter.include_sqlalchemy == "y" %}
1. [Database](./database.md)
{%- endif %}

1. [Dependencies](./dependencies.md)

{%- if cookiecutter.include_docker == "y" %}

1. [Docker](./docker.md)
{%- endif %}
{%- if cookiecutter.include_github_actions == "y" %}
1. [Github Actions](./github.md)
{%- endif %}
{%- if cookiecutter.publish_to_pypi == "y" %}
1. [PyPI](./pypi.md)
{%- endif %}

1. [Settings](./settings.md)

{%- if cookiecutter.include_jinja2 == "y" %}

1. [Templates](./template.md)
{%- endif %}
