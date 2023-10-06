from pydantic_settings import BaseSettings

{%- if cookiecutter.include_sqlalchemy == "y" %}
from .db import DatabaseSettings

class Settings(DatabaseSettings):
{% else %}
class Settings(BaseSettings):
{% endif %}
    project_name: str = "{{ cookiecutter.package_name }}"
    debug: bool = False
