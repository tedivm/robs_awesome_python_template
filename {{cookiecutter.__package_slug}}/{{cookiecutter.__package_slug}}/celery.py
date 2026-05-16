from logging import getLogger
from typing import Any

from celery import Celery  # type: ignore[import-untyped]

{%- if cookiecutter.include_aiocache == "y" %}
from {{cookiecutter.__package_slug}}.services.cache import configure_caches
{%- endif %}

logger = getLogger(__name__)

celery = Celery("{{ cookiecutter.__package_slug }}")


{%- if cookiecutter.include_aiocache == "y" %}
@celery.on_after_configure.connect
def setup_caches(sender: Any, **kwargs: Any) -> None:
    """Initialize caches when Celery worker starts."""
    configure_caches()
{%- endif %}


@celery.task
def hello_world() -> None:
    logger.info("Hello World!")


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender: Any, **kwargs: Any) -> None:
    logger.info("Enabling Test Task")
    sender.add_periodic_task(15.0, hello_world.s(), name="Test Task")
