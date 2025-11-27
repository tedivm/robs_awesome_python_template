import os
{%- if cookiecutter.include_aiocache == "y" %}
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
{%- endif %}

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

{%- if cookiecutter.include_aiocache == "y" %}
from {{cookiecutter.__package_slug}}.settings import settings
from {{cookiecutter.__package_slug}}.services.cache import configure_caches


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage application lifespan events."""
    # Startup: Initialize caches
    configure_caches()
    yield
    # Shutdown: cleanup would go here if needed


app = FastAPI(lifespan=lifespan)
{%- else %}
app = FastAPI()
{%- endif %}

static_file_path = os.path.dirname(os.path.realpath(__file__)) + "/static"
app.mount("/static", StaticFiles(directory=static_file_path), name="static")


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse("/docs")
