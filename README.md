# Rob's Awesome Python Template

Rob's Awesome Python Template is extremely customizable- it can work for the smallest library to the largest application.

- [Rob's Awesome Python Template](#robs-awesome-python-template)
  - [Usage](#usage)
  - [Core Functionality](#core-functionality)
  - [Optional Libraries](#optional-libraries)
    - [FastAPI](#fastapi)
    - [Celery](#celery)
    - [Typer and Click](#typer-and-click)
    - [SQLAlchemy and Alembic](#sqlalchemy-and-alembic)
    - [Docker](#docker)
    - [Github Actions](#github-actions)
  - [Examples](#examples)


## Usage

1. Install `cookiecutter`.
2. Install `pyenv` if you haven't already.
3. Run the cookiecutter command.

```bash
cookiecutter gh:tedivm/robs_awesome_python_template
```

The rest of the process is interactive- you'll be asked for a project name and about which features you want enabled, after which the project will be setup.

## Core Functionality

- Development Management using [Makefiles](https://www.gnu.org/software/make/manual/html_node/Introduction.html).
- Configuration Management with [Pydantic](https://docs.pydantic.dev/usage/settings/).
- PyPI Publishing from Github Tags using [versioneer](https://pypi.org/project/versioneer/).
- Formatting with [Black](https://pypi.org/project/black/).
- Import Sorting with [isort](https://pypi.org/project/isort/).
- Typing with [mypy](https://mypy.readthedocs.io/en/stable/).
- Lockfiles (requirements.txt) with [pip-tools](https://pypi.org/project/pip-tools/).
- Testing with [pytest](https://docs.pytest.org/en/7.2.x/).
- CI/CD using [Github Actions](https://docs.github.com/en/actions).
- Multiple license options.

## Optional Libraries

This template can also configure and setup a variety of optional services. Each optional service adds its own dependencies, configuration, handlers, and everything else needed to jump right into development.

Features that are not selected get completely cleaned up and will not pollute the newly created project.

### FastAPI

[FastAPI](https://fastapi.tiangolo.com/) is one of the easiest ways to develop REST Based APIs. When enabled a "Hello World" application will be setup.

### Celery

[Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) is the standard for Queue Management systems with Python.

### Typer and Click

[Typer](https://typer.tiangolo.com/typer-cli/), which is built on top of the [Click Framework](https://click.palletsprojects.com), is one of the easiest ways to build command line applications. When enabled this template will create an initial CLI handler and register it with python for easy installation.

### SQLAlchemy and Alembic

[SQLAlchemy](https://www.sqlalchemy.org/) is one of the most used SQL ORM frameworks in python. It is regularly paired with [Alembic](https://alembic.sqlalchemy.org/en/latest/) to handle database migrations.

This template configures SQLAlchemy and Alembic to work together using a unified configuration. Alembic will automatically discover all models in the `models` directory.

Projects with this template will have access to the Async SQLAlchemy engine.

### Docker

Docker Images are the standard for distributing and running applications. The Docker extensions to this project create containers for the other services that are enabled, such as FastAPI and Celery.

The images made by this template come from the [Multi-Py](https://github.com/multi-py/) project and support both AMD and ARM architectures.

### Github Actions

Github Action Workflows are optionally created for a variety of tasks-

- Formatting
- Testing
- Typing
- Publishing Packages to PyPI
- Pushing Images to GHCR
- Updating Dependency Files

## Examples

Project examples are available in the [example repository](https://github.com/tedivm/robs_awesome_python_template_examples).

- [Basic Library](https://github.com/tedivm/robs_awesome_python_template_examples/tree/main/library)- enables basic library features without the full scale applications.
- [All Options Enabled](https://github.com/tedivm/robs_awesome_python_template_examples/tree/main/full)- includes every option and service.
- [All Options Disabled](https://github.com/tedivm/robs_awesome_python_template_examples/tree/main/bare)- disabled every optional service for an extremely basic scaffold.

These are just some options, as features can be mixed and matched to create numerous permutations.
