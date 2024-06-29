# API

This project uses [FastAPI](https://fastapi.tiangolo.com/).

Static files can be added to `{{ cookiecutter.__package_slug }}/static` and will be passed through the `/static/` endpoint.


{%- if cookiecutter.include_docker == "y" %}

## Docker

The FastAPI images are based off of the [Multi-Py Uvicorn Project](https://github.com/multi-py/python-uvicorn) and work for ARM and AMD out of the box.

{%- endif %}
