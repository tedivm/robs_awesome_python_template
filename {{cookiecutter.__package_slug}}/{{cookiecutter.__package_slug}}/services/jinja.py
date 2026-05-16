{%- if cookiecutter.include_fastapi == "y" %}
from fastapi.templating import Jinja2Templates
{%- endif %}
from jinja2 import Environment, PackageLoader, select_autoescape
from jinja2.sandbox import SandboxedEnvironment

env = Environment(
    loader=PackageLoader("{{cookiecutter.__package_slug}}"),
    autoescape=True,
)

# Sandboxed environment for untrusted templates (user content, third-party systems).
# Prevents access to Python internals, attribute traversal, and dangerous operations.
sandbox_env = SandboxedEnvironment(
    loader=PackageLoader("{{cookiecutter.__package_slug}}"),
    autoescape=True,
)

{%- if cookiecutter.include_fastapi == "y" %}
response_templates = Jinja2Templates(directory="{{cookiecutter.__package_slug}}/templates")

# Use the primary environment inside of the Jinja2Templates wrapper.
response_templates.env = env
{%- endif %}
