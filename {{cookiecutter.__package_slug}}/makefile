SHELL := /bin/bash
PYTHON := . .venv/bin/activate && python
PYTHON_VERSION := $(shell cat .python-version)
PYTHON_SHORT_VERSION := $(shell cat .python-version | grep -o '[0-9].[0-9]*')
VENV_PACKAGE_CHECK := .venv/lib/python$(PYTHON_SHORT_VERSION)/site-packages/piptools/


.PHONY: all
all: $(VENV_PACKAGE_CHECK)

.venv:
	python -m venv .venv

.PHONY: install
install:
	pyenv install --skip-existing $(PYTHON_VERSION)

$(VENV_PACKAGE_CHECK): install .venv
	$(PYTHON) -m pip install -e .[dev]


#
# Formatting
#

.PHONY: pretty
pretty:
	$(PYTHON) -m black . && \
	isort .

.PHONY: black_fixes
black_fixes:
	$(PYTHON) -m black .

.PHONY: isort_fixes
isort_fixes:
	$(PYTHON) -m isort .


#
# Testing
#

.PHONY: tests
tests: install pytest isort_check black_check mypy_check

.PHONY: pytest
pytest:
	$(PYTHON) -m pytest --cov=./{{cookiecutter.__package_slug}} --cov-report=term-missing tests

.PHONY: pytest_loud
pytest_loud:
	$(PYTHON) -m pytest -s --cov=./{{cookiecutter.__package_slug}} --cov-report=term-missing tests

.PHONY: isort_check
isort_check:
	$(PYTHON) -m isort --check-only .

.PHONY: black_check
black_check:
	$(PYTHON) -m black . --check

.PHONY: mypy_check
mypy_check:
	$(PYTHON) -m mypy {{cookiecutter.__package_slug}}


#
# Dependencies
#

.PHONY: rebuild_dependencies
rebuild_dependencies:
	$(PYTHON) -m piptools compile --output-file=requirements.txt pyproject.toml
	$(PYTHON) -m piptools compile --output-file=requirements-dev.txt --extra=dev pyproject.toml

.PHONY: dependencies
dependencies: requirements.txt requirements-dev.txt

requirements.txt: $(VENV_PACKAGE_CHECK) pyproject.toml
	$(PYTHON) -m piptools compile --upgrade --output-file=requirements.txt pyproject.toml

requirements-dev.txt: $(VENV_PACKAGE_CHECK) pyproject.toml
	$(PYTHON) -m piptools compile --upgrade --output-file=requirements-dev.txt --extra=dev pyproject.toml


#
# Packaging
#

.PHONY: build
build: $(VENV_PACKAGE_CHECK)
	$(PYTHON) -m build

{%- if cookiecutter.include_sqlalchemy == "y" %}

#
# Database
#

.PHONY: create_migration
create_migration:
	@if [ -z "$(MESSAGE)" ]; then echo "Please add a message parameter for the migration (make create_migration MESSAGE=\"database migration notes\")."; exit 1; fi
	rm $(MIGRATION_DATABASE) | true
	. .venv/bin/activate && DATABASE_URL=sqlite:///$(MIGRATION_DATABASE) python -m alembic upgrade head
	. .venv/bin/activate && DATABASE_URL=sqlite:///$(MIGRATION_DATABASE) python -m alembic revision --autogenerate -m "$(MESSAGE)"
	rm $(MIGRATION_DATABASE)

{% endif %}
