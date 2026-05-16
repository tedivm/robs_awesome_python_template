---
name: jinja-templates
description: "Create or modify Jinja2 templates. Use when: adding new HTML templates, configuring the Jinja2 environment, adding custom filters or globals, rendering templates outside FastAPI, or working with template inheritance."
---

# Jinja2 Templates

> **context7**: If the `mcp_context7` tool is available, resolve and load the full `jinja2` documentation before making changes:
> ```
> mcp_context7_resolve-library-id: "pallets/jinja"
> mcp_context7_get-library-docs: <resolved-id>
> ```

The Jinja2 environment is configured in `{{cookiecutter.__package_slug}}/services/jinja.py`. Templates live in `{{cookiecutter.__package_slug}}/templates/`.

---

## Environment

The environment uses `PackageLoader` and `autoescape=True`:

```python
from jinja2 import Environment, PackageLoader

env = Environment(
    loader=PackageLoader("{{cookiecutter.__package_slug}}"),
    autoescape=True,
)
```

{%- if cookiecutter.include_fastapi == "y" %}

For FastAPI responses, use `response_templates`:

```python
from fastapi import Request
from {{cookiecutter.__package_slug}}.services.jinja import response_templates

@app.get("/page")
async def page(request: Request) -> Response:
    return response_templates.TemplateResponse(
        "page.html",
        {"request": request, "title": "Page"},
    )
```

---

{%- endif %}

## Rendering Templates Outside FastAPI

Use the raw `env` for emails, tasks, CLI output:

```python
from {{cookiecutter.__package_slug}}.services.jinja import env

template = env.get_template("emails/welcome.html")
html = template.render(name="World", year=2026)
```

---

## Template Structure

Organize templates in subdirectories:

```
{{cookiecutter.__package_slug}}/templates/
├── base.html           # Base layout
├── pages/
│   └── home.html
├── components/
│   └── header.html
└── emails/
    └── welcome.html
```

---

## Custom Filters and Globals

Add to `{{cookiecutter.__package_slug}}/services/jinja.py`:

```python
def format_currency(value: float) -> str:
    return f"${value:,.2f}"

env.filters["currency"] = format_currency
env.globals["settings"] = settings
```

---

## Template Inheritance

**Base template** (`templates/base.html`):

```html
{%- raw %}
<!DOCTYPE html>
<html>
<head><title>{% block title %}Default{% endblock %}</title></head>
<body>
    {% include "components/header.html" %}
    <main>{% block content %}{% endblock %}</main>
</body>
</html>
{% endraw -%}
```

**Child template** (`templates/pages/home.html`):

```html
{%- raw %}
{% extends "base.html" %}
{% block title %}Home{% endblock %}
{% block content %}<h1>Welcome</h1>{% endblock %}
{% endraw -%}
```

---

## Security

- Autoescape is enabled — user input is automatically HTML-escaped
- Never use `|safe` on user-provided content
- For trusted HTML, use `markupsafe.Markup` in Python or `|safe` in templates

---

## Sandboxed Templates

**Any template whose source comes from users, third-party systems, or external APIs must be rendered with `sandbox_env`, not `env`.**

The standard `env` allows templates to access arbitrary Python attributes and call any function passed to `render()`. A malicious template can exploit this to read secrets, access internals, or execute arbitrary code. The `SandboxedEnvironment` intercepts attribute access, method calls, and operators to prevent these attacks.

| Source | Environment |
| --- | --- |
| Templates in `templates/` (project code) | `env` |
| User-submitted templates | `sandbox_env` |
| Templates from external APIs or plugins | `sandbox_env` |
| Templates stored in the database by users | `sandbox_env` |

For usage patterns, blocked/allowed operations, immutable sandboxing, and customization — see [references/sandboxed-templates.md](references/sandboxed-templates.md).

---

## Style Checklist

- [ ] Templates live in `{{cookiecutter.__package_slug}}/templates/`
- [ ] Custom filters/globals added to `services/jinja.py`
- [ ] Base template used for layout inheritance
- [ ] Components extracted to `components/` subdirectory
- [ ] `|safe` never applied to user input
- [ ] `env` used for non-FastAPI rendering, `response_templates` for FastAPI
- [ ] `sandbox_env` used for ALL user-provided or third-party template content
- [ ] `SecurityError` caught and handled when rendering sandboxed templates

---

## Further Reading

- [docs/dev/templates.md](../../docs/dev/templates.md) — Full Jinja2 developer guide
- [Jinja2 Docs](https://jinja.palletsprojects.com/)
