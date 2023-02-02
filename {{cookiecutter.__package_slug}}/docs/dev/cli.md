# CLI

This project uses [Typer](https://typer.tiangolo.com/) and [Click](https://click.palletsprojects.com/) for CLI functionality. When the project is installed the cli is available at `{{ cookiecutter.__package_slug }}`.

The full help contents can be visited with the help flag.

```bash
{{ cookiecutter.__package_slug }} --help
```

The CLI itself is defined at `{{ cookiecutter.__package_slug }}.cli`. New commands can be added there.
