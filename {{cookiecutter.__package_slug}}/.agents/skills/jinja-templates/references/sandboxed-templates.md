---
name: sandboxed-templates
description: "Full reference for Jinja2 sandboxed template security: usage patterns, blocked/allowed operations, immutable sandboxing, and custom safe attribute/callable overrides."
---

# Sandboxed Templates Reference

Detailed guidance for working with `SandboxedEnvironment` in this project.

---

## Usage

```python
from jinja2.sandbox import SecurityError
from {{cookiecutter.__package_slug}}.services.jinja import sandbox_env

# Render a template string from an untrusted source
try:
    template = sandbox_env.from_string(user_provided_template_string)
    output = template.render(name="World")
except SecurityError:
    # Template tried to access something dangerous — reject it
    pass
```

---

## What the Sandbox Blocks

- Access to any `__*__` attributes (`__class__`, `__code__`, `__dict__`, `__globals__`)
- Access to attributes starting with `_` (private attributes)
- Calling objects marked with `@unsafe` decorator (callables are safe by default)
- Attribute traversal chains that reach into Python internals

---

## What the Sandbox Allows

{% raw %}
- Variable interpolation: `{{ name }}`, `{{ user.name }}`
- Control structures: `{% if %}`, `{% for %}`, `{% include %}`
{% endraw %}
- Built-in filters: `|upper`, `|lower`, `|length`, `|safe`
- Calling functions passed as render context variables

---

## Immutable Sandboxing

Use `ImmutableSandboxedEnvironment` when you also need to prevent templates from modifying data structures passed to `render()`. It blocks mutating method calls on built-in mutable objects (`list.append`, `dict.clear`, `set.pop`, `collections.deque.extend`, etc.) using the `modifies_known_mutable()` check:

```python
from jinja2.sandbox import ImmutableSandboxedEnvironment

{% raw %}
# Prevents templates from doing: {{ items.append("hacked") }}
{% endraw %}
immutable_env = ImmutableSandboxedEnvironment(autoescape=True)
```

---

## Customizing the Sandbox

If you need to allow specific attributes or callables that the sandbox blocks by default, subclass `SandboxedEnvironment` and override its security methods:

```python
from jinja2.sandbox import SandboxedEnvironment, is_internal_attribute

class CustomSandboxedEnvironment(SandboxedEnvironment):
    def is_safe_attribute(self, obj, attr, value):
        # Allow specific attributes that would normally be blocked
        if attr == "custom_attr":
            return True
        # Use the helper to check for internal Python attributes
        if is_internal_attribute(obj, attr):
            return False
        return not attr.startswith("_")

    def is_safe_callable(self, obj):
        # Add custom logic to allow specific callables
        return super().is_safe_callable(obj)
```

---

## Reference

- [Jinja2 Sandbox Docs](https://jinja.palletsprojects.com/en/stable/sandbox/)
- [Jinja2 SandboxedEnvironment API](https://jinja.palletsprojects.com/en/stable/api/#jinja2.sandbox.SandboxedEnvironment)