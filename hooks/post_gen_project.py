import os
import shutil
import subprocess
import sys


INCLUDE_CLI={% if cookiecutter.include_cli == "y" %}True{% else %}False{% endif %}
INCLUDE_CELERY={% if cookiecutter.include_celery == "y" %}True{% else %}False{% endif %}
INCLUDE_FASTAPI={% if cookiecutter.include_fastapi == "y" %}True{% else %}False{% endif %}
INCLUDE_DOCKER={% if cookiecutter.include_docker == "y" %}True{% else %}False{% endif %}
INCLUDE_SQLALCHEMY={% if cookiecutter.include_sqlalchemy == "y" %}True{% else %}False{% endif %}
INCLUDE_GITHUB_ACTIONS={% if cookiecutter.include_github_actions == "y" %}True{% else %}False{% endif %}
PACKAGE_SLUG="{{cookiecutter.__package_slug}}"

remove_paths=set([])
docker_containers=set([])


if INCLUDE_FASTAPI:
    docker_containers.add('www')
else:
    remove_paths.add(f'{PACKAGE_SLUG}/www.py')
    remove_paths.add(f'dockerfile.www')
    remove_paths.add(f'docker/www')

if INCLUDE_CELERY:
    docker_containers.add('celery')
else:
    remove_paths.add(f'{PACKAGE_SLUG}/celery.py')
    remove_paths.add(f'dockerfile.celery')
    remove_paths.add(f'docker/celery')

if not INCLUDE_SQLALCHEMY:
    remove_paths.add(f'{PACKAGE_SLUG}/models')
    remove_paths.add(f'db')
    remove_paths.add(f'services/db.py')
    remove_paths.add(f'alembic.ini')

if not INCLUDE_CLI:
    remove_paths.add(f'{PACKAGE_SLUG}/cli.py')

if not INCLUDE_DOCKER:
    remove_paths.add(f'dockerfile.www')
    remove_paths.add(f'dockerfile.celery')

if not INCLUDE_DOCKER or len(docker_containers) < 1:
    remove_paths.add(f'.github/workflows/docker.yaml')
    remove_paths.add(f'docker')

if not INCLUDE_GITHUB_ACTIONS:
    remove_paths.add(f'.github')

for path in remove_paths:
    path = path.strip()
    if path and os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)


def run_command(command):
    print(f"Running '{command}'")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, )
    for c in iter(lambda: process.stdout.read(1), b""):
        sys.stdout.buffer.write(c)

    returncode = process.wait()
    if returncode != 0:
        print(f"Failed to run command '{command}': {returncode}")
        sys.exit(returncode)


run_command('make dependencies')
run_command('make pretty')
