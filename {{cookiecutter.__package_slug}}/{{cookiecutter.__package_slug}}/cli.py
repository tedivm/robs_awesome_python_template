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

{% if cookiecutter.include_sqlalchemy == "y" %}
@app.command(help="Install testing data for local development.")
@syncify
async def test_data():
    from . import _version
    from .services.db import get_session, test_data

    typer.echo(f"{settings.project_name} - {_version.version}")

    async with get_session() as session:
        await test_data(session)

    typer.echo("Development data installed successfully.")
{% endif %}

@app.command(help=f"Display the current installed version of {settings.project_name}.")
def version():
    from . import _version

    typer.echo(f"{settings.project_name} - {_version.version}")


if __name__ == "__main__":
    app()
