"""Tests for Jinja2 template service."""
import pytest
from jinja2 import Environment
from fastapi.templating import Jinja2Templates
from {{cookiecutter.__package_slug}}.services.jinja import env, response_templates


class TestJinja2Environment:
    """Test Jinja2 environment configuration."""

    def test_env_exists(self):
        """Test that Jinja2 environment is properly instantiated."""
        assert env is not None
        assert isinstance(env, Environment)

    def test_env_has_loader(self):
        """Test that environment has a loader configured."""
        assert env.loader is not None

    def test_env_autoescape_enabled(self):
        """Test that autoescape is enabled for security."""
        assert env.autoescape is True or callable(env.autoescape)

    def test_env_can_compile_template(self):
        """Test that environment can compile a simple template."""
        template = env.from_string("Hello {% raw %}{{ name }}{% endraw %}!")
        result = template.render(name="World")
        assert result == "Hello World!"


class TestJinja2Templates:
    """Test FastAPI Jinja2Templates integration."""

    def test_response_templates_exists(self):
        """Test that response_templates is properly instantiated."""
        assert response_templates is not None
        assert isinstance(response_templates, Jinja2Templates)

    def test_response_templates_has_env(self):
        """Test that response_templates has environment configured."""
        assert hasattr(response_templates, "env")
        assert response_templates.env is not None

    def test_response_templates_uses_custom_env(self):
        """Test that response_templates uses our custom environment."""
        # The custom env should be used instead of default
        assert response_templates.env is env


class TestTemplateLoader:
    """Test template loading functionality."""

    def test_loader_configured_for_package(self):
        """Test that loader is configured for the package."""
        from jinja2 import PackageLoader
        assert isinstance(env.loader, PackageLoader)

    def test_loader_package_name(self):
        """Test that loader is configured with correct package name."""
        assert env.loader.package_name == "{{cookiecutter.__package_slug}}"


class TestTemplateRendering:
    """Test template rendering functionality."""

    def test_simple_template_rendering(self):
        """Test rendering a simple template."""
        template = env.from_string("{% raw %}{{ value }}{% endraw %}")
        result = template.render(value="test")
        assert result == "test"

    def test_template_with_variables(self):
        """Test rendering template with multiple variables."""
        template = env.from_string("{% raw %}{{ name }} is {{ age }} years old{% endraw %}")
        result = template.render(name="Alice", age=30)
        assert result == "Alice is 30 years old"

    def test_template_with_conditionals(self):
        """Test rendering template with conditional logic."""
        template = env.from_string("{% raw %}{% if show %}visible{% else %}hidden{% endif %}{% endraw %}")
        assert template.render(show=True) == "visible"
        assert template.render(show=False) == "hidden"

    def test_template_with_loops(self):
        """Test rendering template with loops."""
        template = env.from_string("{% raw %}{% for i in items %}{{ i }}{% endfor %}{% endraw %}")
        result = template.render(items=[1, 2, 3])
        assert result == "123"


class TestAutoescaping:
    """Test HTML autoescaping functionality."""

    def test_autoescape_escapes_html(self):
        """Test that HTML is properly escaped."""
        template = env.from_string("{% raw %}{{ content }}{% endraw %}")
        result = template.render(content="<script>alert('xss')</script>")
        # Should escape < and >
        assert "&lt;" in result or "<script>" not in result

    def test_autoescape_prevents_xss(self):
        """Test that autoescape prevents XSS attacks."""
        template = env.from_string("{% raw %}{{ user_input }}{% endraw %}")
        dangerous_input = "<img src=x onerror=alert('xss')>"
        result = template.render(user_input=dangerous_input)
        # Should not contain raw script tags
        assert "onerror=" not in result or "&" in result


class TestTemplateFilters:
    """Test Jinja2 built-in filters."""

    def test_upper_filter(self):
        """Test the upper filter."""
        template = env.from_string("{% raw %}{{ text|upper }}{% endraw %}")
        result = template.render(text="hello")
        assert result == "HELLO"

    def test_lower_filter(self):
        """Test the lower filter."""
        template = env.from_string("{% raw %}{{ text|lower }}{% endraw %}")
        result = template.render(text="HELLO")
        assert result == "hello"

    def test_title_filter(self):
        """Test the title filter."""
        template = env.from_string("{% raw %}{{ text|title }}{% endraw %}")
        result = template.render(text="hello world")
        assert result == "Hello World"


class TestTemplateIntegration:
    """Test integration with FastAPI."""

    def test_response_templates_can_render(self):
        """Test that response_templates can render templates."""
        # Create a simple in-memory template
        template = response_templates.env.from_string("Hello {% raw %}{{ name }}{% endraw %}!")
        result = template.render(name="FastAPI")
        assert result == "Hello FastAPI!"

    def test_response_templates_directory_configured(self):
        """Test that response_templates has directory configured."""
        # Jinja2Templates in Starlette stores directory as a string or Path
        assert hasattr(response_templates, "env")
        # The loader should have the templates configured
        assert response_templates.env.loader is not None
