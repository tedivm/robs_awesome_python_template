#!/usr/bin/env bash

echo "FastAPI Prestart Script Running"


{%- if cookiecutter.include_sqlalchemy == "y" %}
echo "Run Database Migrations"
python -m alembic upgrade head
{% endif %}
