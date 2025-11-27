"""Tests for FastAPI web application."""
import pytest
from {{cookiecutter.__package_slug}}.www import app


def test_app_exists():
    """Test that the FastAPI app is properly instantiated."""
    assert app is not None
    assert hasattr(app, "router")


def test_static_files_mounted():
    """Test that static files are properly mounted."""
    routes = [route.path for route in app.routes]
    assert "/static" in routes or any("/static" in route for route in routes)


def test_root_redirects_to_docs(fastapi_client):
    """Test that root path redirects to /docs."""
    response = fastapi_client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/docs"


def test_root_redirect_follows(fastapi_client):
    """Test that following redirect from root goes to docs."""
    response = fastapi_client.get("/", follow_redirects=True)
    assert response.status_code == 200
    # Should reach the OpenAPI docs page


def test_docs_accessible(fastapi_client):
    """Test that /docs endpoint is accessible."""
    response = fastapi_client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


def test_openapi_schema(fastapi_client):
    """Test that OpenAPI schema is accessible."""
    response = fastapi_client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert "paths" in schema


def test_static_route_exists():
    """Test that static route is configured."""
    routes = {route.path: route for route in app.routes}
    # Static files might be mounted at /static or have a prefix
    has_static = any("/static" in path for path in routes.keys())
    assert has_static, "Static files route should be configured"


{%- if cookiecutter.include_aiocache == "y" %}


def test_lifespan_configured():
    """Test that lifespan context manager is configured."""
    # Check that the app has a lifespan handler
    assert app.router.lifespan_context is not None, "Should have lifespan context configured"
{%- endif %}


def test_app_can_start(fastapi_client):
    """Test that the app can start successfully."""
    # Making any request will trigger startup event
    response = fastapi_client.get("/docs")
    assert response.status_code == 200


def test_basic_health(fastapi_client):
    """Test basic application health by accessing root."""
    response = fastapi_client.get("/")
    assert response.status_code in [200, 307], "App should respond to requests"
