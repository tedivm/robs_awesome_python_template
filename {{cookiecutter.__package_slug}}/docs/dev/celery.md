# Celery

This project uses [Celery](https://docs.celeryq.dev/en/stable/) and [Celery Beat](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html).

{%- if cookiecutter.include_docker == "y" %}

## Docker

The Celery images are based off of the [Multi-Py Celery Project](https://github.com/multi-py/python-celery) and work for ARM and AMD out of the box.

For scheduling to work one container has to be launched with [ENABLE_BEAT](https://github.com/multi-py/python-celery#enable_beat) set to `true`.

{%- endif %}
