import os

from invoke import task


@task(aliases=["format"])
def black(c):
    c.run("black klaxon/ tests/ tasks.py")


@task(aliases=["test", "tests"])
def unit_tests(c):
    c.run("pytest --black --mypy tests")


@task
def publish(c):
    """Publish to pypi."""
    username = os.getenv("PYPI_USERNAME")
    password = os.getenv("PYPI_PASSWORD")
    c.run(f"poetry publish -u {username} -p '{password}' --build", pty=True)
