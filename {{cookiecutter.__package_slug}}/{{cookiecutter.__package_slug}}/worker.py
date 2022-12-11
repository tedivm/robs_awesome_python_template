from celery import Celery

celery = Celery("{{ cookiecutter.__package_slug }}")


@celery.task
def hello_world():
    print("Hello World!")


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    print("Enabling Test Task")
    sender.add_periodic_task(15.0, hello_world.s(), name="Test Task")
