import os

from invoke import task


@task
def publish(c):
    """Publish to pypi."""
    username = os.getenv("PYPI_USERNAME")
    password = os.getenv("PYPI_PASSWORD")
    c.run(f"poetry publish -u {username} -p '{password}' --build", pty=True)
