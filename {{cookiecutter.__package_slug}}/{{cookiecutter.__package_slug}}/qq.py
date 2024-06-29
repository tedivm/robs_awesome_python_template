import asyncio

from quasiqueue import QuasiQueue

from .settings import settings


async def writer(desired: int):
  """Feeds data to the Queue when it is low.
  """
  for x in range(0, desired):
    yield x



async def reader(identifier: int|str):
  """Receives individual items from the queue.

  Args:
      identifier (int | str): Comes from the output of the Writer function
  """
  print(f"{identifier}")


runner = QuasiQueue(
  settings.project_name,
  reader=reader,
  writer=writer,
  settings=settings
)

if __name__ == '__main__':
  asyncio.run(runner.main())
