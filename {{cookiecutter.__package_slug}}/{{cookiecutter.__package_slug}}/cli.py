import typer

from .settings import settings

app = typer.Typer()


@app.command(help=f"Display the current installed version of {settings.project_name}.")
def version():
    from . import _version

    typer.echo(f"{settings.project_name} - {_version.version}")


if __name__ == "__main__":
      app()
