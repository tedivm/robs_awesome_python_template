# Docker

## Images

{% if cookiecutter.include_cli == "y" %}

### FastAPI

Images are created using the [Multi-Py Uvicorn Project](https://github.com/multi-py/python-uvicorn).

{% endif %}

{% if cookiecutter.include_celery == "y" %}

### Celery

Images are created using the [Multi-Py Celery Project](https://github.com/multi-py/python-celery).

{% endif %}

## Dev Environment

The build in docker compose environment can be used to development.

{% if cookiecutter.include_github_actions == "y" %}

## Registry

Images are automatically created and published to the Github Container Registry using Github Actions.

{% endif %}
