import asyncio
from collections.abc import AsyncGenerator

from quasiqueue import QuasiQueue

from .settings import settings
{%- if cookiecutter.include_aiocache == "y" %}
from {{cookiecutter.__package_slug}}.services.cache import configure_caches
{%- endif %}


async def writer(desired: int) -> AsyncGenerator[int, None]:
  """Feeds data to the Queue when it is low.
  """
  for x in range(0, desired):
    yield x



async def reader(identifier: int|str) -> None:
  """Receives individual items from the queue.

  Args:
      identifier (int | str): Comes from the output of the Writer function
  """
  print(f"{identifier}")


runner = QuasiQueue(
  settings.project_name,
  reader=reader,  # type: ignore[arg-type]
  writer=writer,  # type: ignore[arg-type]
  settings=settings
)

if __name__ == '__main__':
{%- if cookiecutter.include_aiocache == "y" %}
  # Initialize caches before running QuasiQueue
  configure_caches()
{%- endif %}
  asyncio.run(runner.main())
