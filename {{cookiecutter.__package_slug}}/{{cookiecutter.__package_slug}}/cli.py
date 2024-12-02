import asyncio
from functools import wraps

import typer

from .settings import settings

app = typer.Typer()

def syncify(f):
    """This simple decorator converts an async function into a sync function,
    allowing it to work with Typer.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@app.command(help=f"Display the current installed version of {settings.project_name}.")
def version():
    from . import _version

    typer.echo(f"{settings.project_name} - {_version.version}")


if __name__ == "__main__":
      app()
