import json
import os

import toml
from invoke import task


@task
def install_hooks(c):
    """Install git hooks."""
    c.run("pre-commit install")
    c.run("pre-commit install -t pre-push")


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


@task(check_formatting, mypy, unit_tests)
def publish(c, username=None, password=None):
    """Publish to pypi."""

    username = username or os.getenv("PYPI_USERNAME")

    password = password or os.getenv("PYPI_PASSWORD")

    *_, latest_release = json.loads(c.run("qypi releases klaxon", hide=True).stdout)[
        "klaxon"
    ]

    latest_release_version = latest_release["version"]

    local_version = toml.load("pyproject.toml")["tool"]["poetry"]["version"]

    if local_version == latest_release_version:
        print("local and release version are identical")
    else:
        c.run(f"poetry publish -u {username} -p '{password}' --build", pty=True)
