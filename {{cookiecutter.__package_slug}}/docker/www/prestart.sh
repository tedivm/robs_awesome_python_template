#!/usr/bin/env bash

echo "FastAPI Prestart Script Running"

{% if cookiecutter.include_sqlalchemy == "y" %}
if [ ! -z "$IS_DEV" ]; then
  DB_HOST=$(python -c "from urllib.parse import urlparse; print(urlparse('${DATABASE_URL}').netloc.split('@')[-1]);")
  if [ ! -z "$DB_HOST" ]; then
    while ! nc -zv ${DB_HOST} 5432  > /dev/null 2> /dev/null; do
      echo $DATABASE_URL
      echo "Waiting for postgres to be available at host '${DB_HOST}'"
      sleep 1
    done
  fi
fi

echo "Run Database Migrations"
python -m alembic upgrade head
{% endif %}
