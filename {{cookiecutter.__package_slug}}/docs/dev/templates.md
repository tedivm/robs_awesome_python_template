# Jinja2 Templates

This project uses [Jinja2](https://jinja.palletsprojects.com/), a modern and designer-friendly templating language for Python.

## Overview

Jinja2 is integrated with FastAPI to render HTML templates for web pages, emails, and other text-based content. The template system provides:

- **Template inheritance** for building page layouts
- **Variable interpolation** for dynamic content
- **Control structures** (loops, conditionals)
- **Filters** for transforming data
- **Custom functions** and filters

## Configuration

### Template Location

Templates are stored in the `{{cookiecutter.__package_slug}}/templates/` directory:

```
{{cookiecutter.__package_slug}}/
└── templates/
    ├── base.html           # Base layout template
    ├── index.html          # Homepage template
    ├── components/
    │   ├── header.html     # Reusable header
    │   └── footer.html     # Reusable footer
    └── emails/
        └── welcome.html    # Email templates
```

### Jinja2 Environment

The Jinja2 environment is configured in `{{cookiecutter.__package_slug}}/services/jinja.py`:

```python
from jinja2 import Environment, PackageLoader, select_autoescape

# Create Jinja2 environment
env = Environment(
    loader=PackageLoader("{{cookiecutter.__package_slug}}", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
    trim_blocks=True,
    lstrip_blocks=True,
)
```

{%- if cookiecutter.include_fastapi == "y" %}

### FastAPI Integration

In FastAPI routes, use the Jinja2Templates class:

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="{{cookiecutter.__package_slug}}/templates")

@app.get("/")
async def homepage(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Welcome"}
    )
```

{%- endif %}

## Basic Template Usage

### Simple Template

Create a basic template (`templates/hello.html`):

```html
{%- raw %}
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>Hello, {{ name }}!</h1>
    <p>Welcome to {{ project_name }}</p>
</body>
</html>
{% endraw -%}
```

Render in a route:

```python
@app.get("/hello/{name}")
async def hello(request: Request, name: str):
    return templates.TemplateResponse(
        "hello.html",
        {
            "request": request,
            "title": f"Hello {name}",
            "name": name,
            "project_name": "My Application"
        }
    )
```

### Variables

Use double curly braces for variable interpolation:

```html
{%- raw %}
{{ variable }}                    <!-- Simple variable -->
{{ user.name }}                   <!-- Object attribute -->
{{ items[0] }}                    <!-- List/dict access -->
{{ data['key'] }}                 <!-- Dictionary access -->
{{ function() }}                  <!-- Function call -->
{% endraw -%}
```

### Comments

```html
{%- raw %}
{# This is a comment and won't appear in output #}

{#
Multi-line
comment
#}
{% endraw -%}
```

## Template Inheritance

### Base Template

Create a base layout (`templates/base.html`):

```html
{%- raw %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Default Title{% endblock %}</title>

    <link rel="stylesheet" href="/static/css/style.css">

    {% block extra_head %}{% endblock %}
</head>
<body>
    <header>
        {% include 'components/header.html' %}
    </header>

    <main>
        {% block content %}
        <p>Default content</p>
        {% endblock %}
    </main>

    <footer>
        {% include 'components/footer.html' %}
    </footer>

    {% block extra_scripts %}{% endblock %}
</body>
</html>
{% endraw -%}
```

### Child Template

Extend the base template (`templates/page.html`):

```html
{%- raw %}
{% extends "base.html" %}

{% block title %}My Page Title{% endblock %}

{% block extra_head %}
<link rel="stylesheet" href="/static/css/page-specific.css">
{% endblock %}

{% block content %}
<h1>Welcome to My Page</h1>
<p>This content replaces the default content block.</p>
{% endblock %}

{% block extra_scripts %}
<script src="/static/js/page-specific.js"></script>
{% endblock %}
{% endraw -%}
```

## Control Structures

### Conditionals

```html
{%- raw %}
{% if user.is_authenticated %}
    <p>Welcome back, {{ user.name }}!</p>
{% elif user.is_guest %}
    <p>Welcome, guest!</p>
{% else %}
    <p>Please log in.</p>
{% endif %}
{% endraw -%}
```

### Loops

```html
{%- raw %}
<ul>
{% for item in items %}
    <li>{{ loop.index }}: {{ item.name }}</li>
{% endfor %}
</ul>

<!-- Loop with else (when list is empty) -->
<ul>
{% for user in users %}
    <li>{{ user.name }}</li>
{% else %}
    <li>No users found.</li>
{% endfor %}
</ul>

<!-- Loop variables -->
{% for item in items %}
    {{ loop.index }}      <!-- 1, 2, 3, ... -->
    {{ loop.index0 }}     <!-- 0, 1, 2, ... -->
    {{ loop.first }}      <!-- True on first iteration -->
    {{ loop.last }}       <!-- True on last iteration -->
    {{ loop.length }}     <!-- Total number of items -->
{% endfor %}
{% endraw -%}
```

### Filters

Transform variables with filters:

```html
{%- raw %}
{{ name|upper }}                  <!-- Convert to uppercase -->
{{ text|lower }}                  <!-- Convert to lowercase -->
{{ number|abs }}                  <!-- Absolute value -->
{{ items|length }}                <!-- Get length -->
{{ price|round(2) }}              <!-- Round to 2 decimals -->
{{ html_content|safe }}           <!-- Mark as safe (no escaping) -->
{{ description|truncate(100) }}   <!-- Truncate to 100 chars -->
{{ date|default("N/A") }}         <!-- Default if undefined -->
{{ items|join(", ") }}            <!-- Join list with separator -->
{{ text|replace("old", "new") }}  <!-- Replace text -->
{% endraw -%}
```

## Custom Filters

### Adding Filters

Add custom filters to the Jinja2 environment:

```python
# {{cookiecutter.__package_slug}}/services/jinja.py
from jinja2 import Environment, PackageLoader
from datetime import datetime

env = Environment(loader=PackageLoader("{{cookiecutter.__package_slug}}", "templates"))

def format_datetime(value, format="%Y-%m-%d %H:%M:%S"):
    """Format datetime object."""
    if isinstance(value, datetime):
        return value.strftime(format)
    return value

def currency(value):
    """Format as currency."""
    return f"${value:,.2f}"

# Register custom filters
env.filters["datetime"] = format_datetime
env.filters["currency"] = currency
```

Usage in templates:

```html
{%- raw %}
<p>Date: {{ created_at|datetime("%B %d, %Y") }}</p>
<p>Price: {{ amount|currency }}</p>
{% endraw -%}
```

### Common Custom Filters

```python
def pluralize(count, singular, plural=None):
    """Return singular or plural form based on count."""
    if plural is None:
        plural = singular + "s"
    return singular if count == 1 else plural

def markdown_to_html(text):
    """Convert Markdown to HTML."""
    import markdown
    return markdown.markdown(text)

def nl2br(text):
    """Convert newlines to <br> tags."""
    return text.replace("\n", "<br>")

# Register filters
env.filters["pluralize"] = pluralize
env.filters["markdown"] = markdown_to_html
env.filters["nl2br"] = nl2br
```

## Custom Functions

### Global Functions

Add functions available in all templates:

```python
# {{cookiecutter.__package_slug}}/services/jinja.py
from {{cookiecutter.__package_slug}}.conf import settings

def url_for(endpoint: str, **params) -> str:
    """Generate URL for endpoint."""
    # URL generation logic
    return f"/{endpoint}"

def asset_url(path: str) -> str:
    """Generate URL for static asset."""
    return f"/static/{path}"

# Register global functions
env.globals["url_for"] = url_for
env.globals["asset_url"] = asset_url
env.globals["settings"] = settings  # Access settings in templates
```

Usage in templates:

```html
{%- raw %}
<a href="{{ url_for('users', id=123) }}">User Profile</a>
<img src="{{ asset_url('images/logo.png') }}" alt="Logo">
<p>App Name: {{ settings.project_name }}</p>
{% endraw -%}
```

## Template Components

### Including Templates

Reuse template fragments with `include`:

```html
{%- raw %}
<!-- templates/components/header.html -->
<header>
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
    </nav>
</header>

<!-- templates/page.html -->
{% include 'components/header.html' %}
<main>
    <p>Page content here</p>
</main>
{% endraw -%}
```

### Macros

Create reusable template functions with macros:

```html
{%- raw %}
<!-- templates/macros/forms.html -->
{% macro input(name, type="text", placeholder="", required=false) %}
<div class="form-group">
    <input
        type="{{ type }}"
        name="{{ name }}"
        placeholder="{{ placeholder }}"
        {% if required %}required{% endif %}
    >
</div>
{% endmacro %}

{% macro button(text, type="submit", classes="btn-primary") %}
<button type="{{ type }}" class="btn {{ classes }}">
    {{ text }}
</button>
{% endmacro %}

<!-- templates/form.html -->
{% from 'macros/forms.html' import input, button %}

<form method="post">
    {{ input('username', placeholder='Enter username', required=true) }}
    {{ input('password', type='password', placeholder='Enter password', required=true) }}
    {{ button('Login') }}
</form>
{% endraw -%}
```

## Rendering Templates Outside FastAPI

### Direct Rendering

Render templates in other contexts (tasks, CLI, emails):

```python
from {{cookiecutter.__package_slug}}.services.jinja import env

def send_welcome_email(user_email: str, user_name: str):
    """Send welcome email using template."""
    template = env.get_template("emails/welcome.html")
    html_content = template.render(
        name=user_name,
        email=user_email,
        year=2024,
    )

    # Send email with html_content
    send_email(user_email, "Welcome!", html_content)
```

### Celery Tasks

Use templates in Celery tasks:

```python
from {{cookiecutter.__package_slug}}.celery import celery
from {{cookiecutter.__package_slug}}.services.jinja import env

@celery.task
def generate_report(report_id: int):
    """Generate HTML report."""
    template = env.get_template("reports/monthly.html")

    # Get report data
    data = fetch_report_data(report_id)

    # Render template
    html = template.render(
        report_id=report_id,
        data=data,
        generated_at=datetime.now(),
    )

    # Save or send report
    save_report(report_id, html)
```

## Autoescape

### HTML Escaping

By default, variables are HTML-escaped for security:

```html
{%- raw %}
{{ user_input }}  <!-- Automatically escaped -->

<!-- If user_input is "<script>alert('xss')</script>" -->
<!-- Output: &lt;script&gt;alert(&#39;xss&#39;)&lt;/script&gt; -->
{% endraw -%}
```

### Marking Safe Content

Mark trusted content as safe to bypass escaping:

```python
from markupsafe import Markup

@app.get("/page")
async def page(request: Request):
    safe_html = Markup("<strong>Bold text</strong>")
    return templates.TemplateResponse(
        "page.html",
        {"request": request, "content": safe_html}
    )
```

Or in the template:

```html
{%- raw %}
{{ content|safe }}  <!-- Disable escaping with safe filter -->
{% endraw -%}
```

## Error Handling

### Template Not Found

Handle missing templates gracefully:

```python
from jinja2 import TemplateNotFound

@app.get("/page/{name}")
async def dynamic_page(request: Request, name: str):
    try:
        return templates.TemplateResponse(
            f"pages/{name}.html",
            {"request": request}
        )
    except TemplateNotFound:
        return templates.TemplateResponse(
            "404.html",
            {"request": request},
            status_code=404
        )
```

### Debug Mode

Enable debug mode during development:

```python
env = Environment(
    loader=PackageLoader("{{cookiecutter.__package_slug}}", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
    auto_reload=True,  # Reload templates on change (development only)
)
```

## Best Practices

1. **Use Template Inheritance**: Create a base layout and extend it for consistency across pages

2. **Separate Concerns**: Keep logic in Python code, use templates for presentation only

3. **Escape User Input**: Never use `|safe` on user-provided content - risk of XSS attacks

4. **Organize Templates**: Group related templates in subdirectories:

   ```text
   templates/
   ├── base.html
   ├── pages/
   │   ├── home.html
   │   └── about.html
   ├── components/
   │   ├── header.html
   │   └── footer.html
   └── emails/
       └── welcome.html
   ```

5. **Use Macros for Repetitive HTML**: Create macros for common components like forms, buttons, cards

6. **Cache Templates in Production**: Disable `auto_reload` in production for better performance

7. **Pass Context Explicitly**: Always pass data explicitly rather than relying on globals:

   ```python
   # Good
   templates.TemplateResponse("page.html", {"request": request, "user": user})

   # Bad - implicit global access
   ```

## Development vs Production

### Development

```python
# Development environment with auto-reload
env = Environment(
    loader=PackageLoader("{{cookiecutter.__package_slug}}", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
    auto_reload=True,      # Reload on changes
    cache_size=0,           # Disable caching
)
```

### Production

```python
# Production environment optimized for performance
env = Environment(
    loader=PackageLoader("{{cookiecutter.__package_slug}}", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
    auto_reload=False,     # Don't reload
    cache_size=400,         # Cache compiled templates
    trim_blocks=True,
    lstrip_blocks=True,
)
```

## Testing Templates

### Testing Jinja2 Environment

Test that the Jinja2 environment is properly configured:

```python
# tests/services/test_jinja.py
from jinja2 import Environment
from fastapi.templating import Jinja2Templates
from {{cookiecutter.__package_slug}}.services.jinja import env, response_templates


def test_env_exists():
    """Test that Jinja2 environment is properly instantiated."""
    assert env is not None
    assert isinstance(env, Environment)


def test_env_has_loader():
    """Test that environment has a loader configured."""
    assert env.loader is not None


def test_env_autoescape_enabled():
    """Test that autoescape is enabled for security."""
    assert env.autoescape is True or callable(env.autoescape)


def test_response_templates_exists():
    """Test that response_templates is properly instantiated."""
    assert response_templates is not None
    assert isinstance(response_templates, Jinja2Templates)


def test_response_templates_uses_custom_env():
    """Test that response_templates uses our custom environment."""
    assert response_templates.env is env
```

### Testing Template Rendering

Test that templates can be compiled and rendered:

```python
def test_env_can_compile_template():
    """Test that environment can compile a simple template."""
    template = env.from_string("{%- raw %}Hello {{ name }}!{% endraw -%}")
    result = template.render(name="World")
    assert result == "Hello World!"


def test_template_rendering_with_variables():
    """Test template rendering with multiple variables."""
    template = env.from_string("""{%- raw %}
    <h1>{{ title }}</h1>
    <p>Welcome, {{ user }}!</p>
    {% endraw -%}""")

    output = template.render(title="Dashboard", user="John")
    assert "<h1>Dashboard</h1>" in output
    assert "Welcome, John!" in output
```

### Testing Template Loops and Conditionals

Test template control structures:

```python
def test_template_with_loop():
    """Test template with for loop."""
    template = env.from_string("""{%- raw %}
    <ul>
    {% for item in items %}
    <li>{{ item }}</li>
    {% endfor %}
    </ul>
    {% endraw -%}""")

    output = template.render(items=["Apple", "Banana", "Cherry"])
    assert "<li>Apple</li>" in output
    assert "<li>Banana</li>" in output
    assert "<li>Cherry</li>" in output


def test_template_with_conditional():
    """Test template with if statement."""
    template = env.from_string("""{%- raw %}
    {% if user.is_admin %}
    <p>Admin Panel</p>
    {% else %}
    <p>User Panel</p>
    {% endif %}
    {% endraw -%}""")

    # Test admin path
    output = template.render(user={"is_admin": True})
    assert "Admin Panel" in output

    # Test user path
    output = template.render(user={"is_admin": False})
    assert "User Panel" in output
```

### Testing Template Filters

Test that filters work correctly:

```python
def test_template_upper_filter():
    """Test upper filter."""
    template = env.from_string("{%- raw %}{{ text|upper }}{% endraw -%}")
    result = template.render(text="hello")
    assert result == "HELLO"


def test_template_default_filter():
    """Test default filter."""
    template = env.from_string("{%- raw %}{{ value|default('N/A') }}{% endraw -%}")

    # With value
    result = template.render(value="Something")
    assert result == "Something"

    # Without value
    result = template.render(value=None)
    assert result == "N/A"


def test_template_length_filter():
    """Test length filter."""
    template = env.from_string("{%- raw %}{{ items|length }}{% endraw -%}")
    result = template.render(items=[1, 2, 3, 4, 5])
    assert result == "5"
```

### Testing Custom Filters

Test custom filters added to the environment:

```python
def test_custom_filter_registered():
    """Test that custom filters are registered."""
    # If you added a custom 'currency' filter
    assert "currency" in env.filters


def test_custom_currency_filter():
    """Test custom currency filter."""
    # Add the filter first (or ensure it's in services/jinja.py)
    def currency(value):
        return f"${value:,.2f}"

    env.filters["currency"] = currency

    template = env.from_string("{%- raw %}{{ amount|currency }}{% endraw -%}")
    result = template.render(amount=1234.56)
    assert result == "$1,234.56"
```

### Testing Template Loading

Test that templates can be loaded from files:

```python
def test_template_loader_can_find_templates():
    """Test that loader can locate templates."""
    # Assumes you have a test template in templates/
    template_source = env.loader.get_source(env, "base.html")
    assert template_source is not None


def test_can_load_template_from_file():
    """Test loading a template file."""
    # This will raise TemplateNotFound if template doesn't exist
    template = env.get_template("base.html")
    assert template is not None
```

### Testing Template Inheritance

Test that template inheritance works correctly:

```python
def test_template_inheritance():
    """Test template extends and blocks."""
    # Create base template
    base = env.from_string("""{%- raw %}
    <html>
    <head>{% block title %}Default Title{% endblock %}</head>
    <body>{% block content %}Default Content{% endblock %}</body>
    </html>
    {% endraw -%}""")

    # Create child template
    child = env.from_string("""{%- raw %}
    {% extends base %}
    {% block title %}Custom Title{% endblock %}
    {% block content %}Custom Content{% endblock %}
    {% endraw -%}""")

    output = child.render(base=base)
    assert "Custom Title" in output
    assert "Custom Content" in output
```

### Testing Template Security (Autoescape)

Test that HTML is properly escaped:

```python
def test_autoescape_prevents_xss():
    """Test that HTML is escaped by default."""
    template = env.from_string("{%- raw %}<p>{{ user_input }}</p>{% endraw -%}")

    # Potentially malicious input
    result = template.render(user_input="<script>alert('xss')</script>")

    # Should be escaped
    assert "&lt;script&gt;" in result
    assert "<script>" not in result


def test_safe_filter_disables_escaping():
    """Test that |safe filter prevents escaping."""
    template = env.from_string("{%- raw %}{{ content|safe }}{% endraw -%}")

    result = template.render(content="<strong>Bold</strong>")

    # Should NOT be escaped
    assert "<strong>Bold</strong>" in result
```

{%- if cookiecutter.include_fastapi == "y" %}

### Testing with FastAPI Routes

Test templates rendered in FastAPI routes using the `fastapi_client` fixture:

```python
def test_template_response_in_route(fastapi_client):
    """Test that route returns rendered template."""
    response = fastapi_client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_template_variables_in_route(fastapi_client):
    """Test that template variables are rendered in route."""
    response = fastapi_client.get("/profile/john")

    assert response.status_code == 200
    assert "john" in response.text.lower()
```

{%- endif %}

## References

- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Jinja2 Template Designer Documentation](https://jinja.palletsprojects.com/templates/)
- [FastAPI Templates](https://fastapi.tiangolo.com/advanced/templates/)
- [MarkupSafe Documentation](https://markupsafe.palletsprojects.com/)
