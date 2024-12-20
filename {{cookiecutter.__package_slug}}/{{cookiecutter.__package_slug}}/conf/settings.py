{%- if cookiecutter.include_quasiqueue == "n" and  cookiecutter.include_sqlalchemy == "n"%}
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
{%- else %}
{%- set settings_classes = [] %}
{%- if cookiecutter.include_quasiqueue == "y" %}
from quasiqueue import Settings as QuasiQueueSettings
{{- settings_classes.append("QuasiQueueSettings") or "" }}
{% endif %}
{%- if cookiecutter.include_sqlalchemy == "y" %}
from .db import DatabaseSettings
{{- settings_classes.append("DatabaseSettings") or "" }}
{% endif %}

class Settings({{ settings_classes|join(", ") }}):
{%- endif %}
    project_name: str = "{{ cookiecutter.package_name }}"
    debug: bool = False
