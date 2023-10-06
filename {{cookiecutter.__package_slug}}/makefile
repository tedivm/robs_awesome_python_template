SHELL := /bin/bash
{%- if cookiecutter.include_sqlalchemy == "y" %}
MIGRATION_DATABASE:=./migrate.db
{% endif %}
PACKAGE_SLUG={{cookiecutter.__package_slug}}
ifdef CI
	PYTHON_PYENV :=
	PYTHON_VERSION := $(shell python --version|cut -d" " -f2)
else
	PYTHON_PYENV := pyenv
	PYTHON_VERSION := $(shell cat .python-version)
endif
PYTHON_SHORT_VERSION := $(shell echo $(PYTHON_VERSION) | grep -o '[0-9].[0-9]*')

ifeq ($(USE_SYSTEM_PYTHON), true)
	PYTHON_PACKAGE_PATH:=$(shell python -c "import sys; print(sys.path[-1])")
	PYTHON_ENV :=
	PYTHON := python
	PYTHON_VENV :=
else
	PYTHON_PACKAGE_PATH:=.venv/lib/python$(PYTHON_SHORT_VERSION)/site-packages
	PYTHON_ENV :=  . .venv/bin/activate &&
	PYTHON := . .venv/bin/activate && python
	PYTHON_VENV := .venv
endif

# Used to confirm that pip has run at least once
PACKAGE_CHECK:=$(PYTHON_PACKAGE_PATH)/piptools
PYTHON_DEPS := $(PACKAGE_CHECK)


.PHONY: all
all: $(PACKAGE_CHECK)

.PHONY: install
install: $(PYTHON_PYENV) $(PYTHON_VENV) pip

.venv:
	python -m venv .venv

.PHONY: pyenv
pyenv:
	pyenv install --skip-existing $(PYTHON_VERSION)

pip: $(PYTHON_VENV)
	$(PYTHON) -m pip install -e .[dev]

$(PACKAGE_CHECK): $(PYTHON_VENV)
	$(PYTHON) -m pip install -e .[dev]

pre-commit:
  pre-commit install

#
# Formatting
#

.PHONY: pretty
pretty: black_fixes isort_fixes dapperdata_fixes tomlsort_fixes

.PHONY: black_fixes
black_fixes:
	$(PYTHON) -m black .

.PHONY: isort_fixes
isort_fixes:
	$(PYTHON) -m isort .

.PHONY: dapperdata_fixes
dapperdata_fixes:
	$(PYTHON) -m dapperdata.cli pretty . --no-dry-run

.PHONY: tomlsort_fixes
tomlsort_fixes:
	$(PYTHON_ENV) toml-sort $$(find . -not -path "./.venv/*" -name "*.toml") -i

#
# Testing
#

.PHONY: tests
tests: install pytest isort_check black_check mypy_check dapperdata_check tomlsort_check

.PHONY: pytest
pytest:
	$(PYTHON) -m pytest --cov=./${PACKAGE_SLUG} --cov-report=term-missing tests

.PHONY: pytest_loud
pytest_loud:
	$(PYTHON) -m pytest -s --cov=./${PACKAGE_SLUG} --cov-report=term-missing tests

.PHONY: isort_check
isort_check:
	$(PYTHON) -m isort --check-only .

.PHONY: black_check
black_check:
	$(PYTHON) -m black . --check

.PHONY: mypy_check
mypy_check:
	$(PYTHON) -m mypy ${PACKAGE_SLUG}

.PHONY: dapperdata_check
dapperdata_check:
	$(PYTHON) -m dapperdata.cli pretty .

.PHONY: tomlsort_check
tomlsort_check:
	$(PYTHON_ENV) toml-sort $$(find . -not -path "./.venv/*" -name "*.toml") --check



{%- if cookiecutter.include_requirements_files == "y" %}
#
# Dependencies
#

.PHONY: rebuild_dependencies
rebuild_dependencies:
	$(PYTHON) -m piptools compile --resolver=backtracking --output-file=requirements.txt pyproject.toml
	$(PYTHON) -m piptools compile --resolver=backtracking --output-file=requirements-dev.txt --extra=dev pyproject.toml

.PHONY: dependencies
dependencies: requirements.txt requirements-dev.txt

requirements.txt: $(PACKAGE_CHECK) pyproject.toml
	$(PYTHON) -m piptools compile --resolver=backtracking --upgrade --output-file=requirements.txt pyproject.toml

requirements-dev.txt: $(PACKAGE_CHECK) pyproject.toml
	$(PYTHON) -m piptools compile --resolver=backtracking --upgrade --output-file=requirements-dev.txt --extra=dev pyproject.toml


{% endif %}
#
# Packaging
#

.PHONY: build
build: $(PACKAGE_CHECK)
	$(PYTHON) -m build

{%- if cookiecutter.include_sqlalchemy == "y" %}

#
# Database
#

.PHONY: run_migrations
run_migrations:
	$(PYTHON) -m alembic upgrade head

.PHONY: reset_db
reset_db: clear_db run_migrations

.PHONY: clear_db
clear_db:
	rm -Rf test.db*

.PHONY: create_migration
create_migration:
	@if [ -z "$(MESSAGE)" ]; then echo "Please add a message parameter for the migration (make create_migration MESSAGE=\"database migration notes\")."; exit 1; fi
	rm $(MIGRATION_DATABASE) | true
	. .venv/bin/activate && DATABASE_URL=sqlite:///$(MIGRATION_DATABASE) python -m alembic upgrade head
	. .venv/bin/activate && DATABASE_URL=sqlite:///$(MIGRATION_DATABASE) python -m alembic revision --autogenerate -m "$(MESSAGE)"
	rm $(MIGRATION_DATABASE)
	$(PYTHON) -m isort ./db
	$(PYTHON) -m black ./db


{% endif %}
