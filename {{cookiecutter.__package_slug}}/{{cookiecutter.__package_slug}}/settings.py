from pydantic import BaseSettings


class Settings(BaseSettings):
    project_name: str = "{{ cookiecutter.package_name }}"
{%- if cookiecutter.include_sqlalchemy == "y" %}
    database_url: str = "sqlite:///./test.db"
{% endif %}


settings = Settings()
