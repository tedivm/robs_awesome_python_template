{%- set base_classes = [] -%}
{%- if cookiecutter.include_quasiqueue.lower() == "y" %}
from quasiqueue import Settings as QuasiQueueSettings
{{- base_classes.append("QuasiQueueSettings") or "" -}}
{%- endif %}
{%- if cookiecutter.include_sqlalchemy.lower() == "y" %}
from .db import DatabaseSettings
{{- base_classes.append("DatabaseSettings") or "" -}}
{%- endif %}
{%- if cookiecutter.include_aiocache == "y" %}
from .cache import CacheSettings
{{- base_classes.append("CacheSettings") or "" -}}
{%- endif %}
{%- if base_classes|length == 0 %}
from pydantic_settings import BaseSettings
{{- base_classes.append("BaseSettings") or "" -}}
{%- endif %}


class Settings({{ base_classes|join(", ") }}):
    project_name: str = "{{ cookiecutter.package_name }}"
    debug: bool = False
