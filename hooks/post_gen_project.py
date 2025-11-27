import os
import shutil
import subprocess
import sys


INCLUDE_CLI={% if cookiecutter.include_cli == "y" %}True{% else %}False{% endif %}
INCLUDE_CELERY={% if cookiecutter.include_celery == "y" %}True{% else %}False{% endif %}
INCLUDE_FASTAPI={% if cookiecutter.include_fastapi == "y" %}True{% else %}False{% endif %}
INCLUDE_DOCKER={% if cookiecutter.include_docker == "y" %}True{% else %}False{% endif %}
INCLUDE_QUASIQUEUE={% if cookiecutter.include_quasiqueue == "y" %}True{% else %}False{% endif %}
INCLUDE_JINJA2={% if cookiecutter.include_jinja2 == "y" %}True{% else %}False{% endif %}
INCLUDE_AIOCACHE={% if cookiecutter.include_aiocache == "y" %}True{% else %}False{% endif %}
INCLUDE_SQLALCHEMY={% if cookiecutter.include_sqlalchemy == "y" %}True{% else %}False{% endif %}
INCLUDE_GITHUB_ACTIONS={% if cookiecutter.include_github_actions == "y" %}True{% else %}False{% endif %}
INCLUDE_REQUIREMENTS_FILES={% if cookiecutter.include_requirements_files == "y" %}True{% else %}False{% endif %}
INCLUDE_AGENT_INSTRUCTIONS={% if cookiecutter.include_agents_instructions == "y" %}True{% else %}False{% endif %}
PUBLISH_TO_PYPI={% if cookiecutter.publish_to_pypi == "y" %}True{% else %}False{% endif %}
PACKAGE_SLUG="{{cookiecutter.__package_slug}}"

remove_paths=set([])
docker_containers=set([])
CHECK_FOR_EMPTY_DIRS = [f'{PACKAGE_SLUG}/services', 'docs/dev', 'docs']

if INCLUDE_FASTAPI:
    docker_containers.add('www')
else:
    remove_paths.add(f'{PACKAGE_SLUG}/www.py')
    remove_paths.add(f'{PACKAGE_SLUG}/static')
    remove_paths.add(f'dockerfile.www')
    remove_paths.add(f'docker/www')
    remove_paths.add(f'docs/dev/api.md')
    remove_paths.add(f'tests/test_www.py')

if INCLUDE_CELERY:
    docker_containers.add('celery')
else:
    remove_paths.add(f'{PACKAGE_SLUG}/celery.py')
    remove_paths.add(f'dockerfile.celery')
    remove_paths.add(f'docker/celery')
    remove_paths.add(f'docs/dev/celery.md')
    remove_paths.add(f'tests/test_celery.py')

if INCLUDE_QUASIQUEUE:
    docker_containers.add('qq')
else:
    remove_paths.add(f'{PACKAGE_SLUG}/qq.py')
    remove_paths.add(f'dockerfile.qq')
    remove_paths.add(f'docs/dev/quasiqueue.md')
    remove_paths.add(f'tests/test_qq.py')

if not INCLUDE_SQLALCHEMY:
    remove_paths.add(f'{PACKAGE_SLUG}/models')
    remove_paths.add('db')
    remove_paths.add(f'{PACKAGE_SLUG}/conf/db.py')
    remove_paths.add(f'{PACKAGE_SLUG}/services/db.py')
    remove_paths.add('alembic.ini')
    remove_paths.add(f'docs/dev/database.md')
    remove_paths.add(f'.github/workflows/alembic.yaml')
    remove_paths.add(f'.github/workflows/paracelsus.yaml')

if not INCLUDE_CLI:
    remove_paths.add(f'{PACKAGE_SLUG}/cli.py')
    remove_paths.add(f'docs/dev/cli.md')
    remove_paths.add(f'tests/test_cli.py')

if not INCLUDE_JINJA2:
    remove_paths.add(f'{PACKAGE_SLUG}/templates')
    remove_paths.add(f'{PACKAGE_SLUG}/services/jinja.py')
    remove_paths.add(f'docs/dev/templates.md')
    remove_paths.add(f'tests/services/test_jinja.py')

if not INCLUDE_AIOCACHE:
    remove_paths.add(f'{PACKAGE_SLUG}/conf/cache.py')
    remove_paths.add(f'{PACKAGE_SLUG}/services/cache.py')
    remove_paths.add(f'tests/services/test_cache.py')
    remove_paths.add(f'docs/dev/cache.md')

# Always include test_settings.py as it tests core settings functionality
# that exists regardless of optional features

if not INCLUDE_DOCKER:
    remove_paths.add('.dockerignore')
    remove_paths.add('compose.yaml')
    remove_paths.add('dockerfile.www')
    remove_paths.add('dockerfile.celery')
    remove_paths.add('dockerfile.qq')
    remove_paths.add(f'docs/dev/docker.md')

if not INCLUDE_DOCKER or len(docker_containers) < 1:
    remove_paths.add('.github/workflows/docker.yaml')
    remove_paths.add('docker')

if not INCLUDE_GITHUB_ACTIONS:
    remove_paths.add('.github')
    remove_paths.add(f'docs/dev/github.md')

if not INCLUDE_REQUIREMENTS_FILES:
    remove_paths.add('.github/workflows/lockfiles.yaml')
    remove_paths.add(f'docs/dev/dependencies.md')

if not INCLUDE_AGENT_INSTRUCTIONS:
    remove_paths.add(f'AGENTS.md')

for path in remove_paths:
    path = path.strip()
    if path and os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)

# Check for empty directories
for path in CHECK_FOR_EMPTY_DIRS:
    path = path.strip()
    if path and os.path.exists(path):
        if os.path.isdir(path):
            if len(os.listdir(path)) == 0:
                shutil.rmtree(path)


def run_command(command):
    print(f"Running '{command}'")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, )
    for c in iter(lambda: process.stdout.read(1), b""):
        sys.stdout.buffer.write(c)

    returncode = process.wait()
    if returncode != 0:
        print(f"Failed to run command '{command}': {returncode}")
        sys.exit(returncode)


run_command('make all')
if INCLUDE_REQUIREMENTS_FILES:
   run_command('make dependencies')
run_command('make chores')
