import os

from invoke import task


@task
def echo(c, word="hello"):
    """Here for testing."""
    c.run(f"echo {word}")


@task(aliases=["format"])
def black(c):
    """Format modules using black."""
    c.run("black klaxon/ tests/ tasks.py")


@task(aliases=["check-black"])
def check_formatting(c):
    """Check that files conform to black standards."""
    c.run("black --check klaxon/ tests/ tasks.py")


@task
def mypy(c):
    """Type-check code."""
    c.run("mypy klaxon/ tests/ tasks.py --ignore-missing-imports")


@task
def unit_tests(c):
    """Run unit tests via pytest."""
    c.run("pytest tests/")


@task
def publish(c):
    """Publish to pypi."""
    username = os.getenv("PYPI_USERNAME")
    password = os.getenv("PYPI_PASSWORD")
    c.run(f"poetry publish -u {username} -p '{password}' --build", pty=True)
