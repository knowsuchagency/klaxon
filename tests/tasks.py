from invoke import task
from klaxon.invoke import klaxonify


@task
@klaxonify
def succeed(c):
    ...


@task
@klaxonify
def fail_normally(c):
    raise ValueError("derp")


@task
@klaxonify
def fail_badly(c):
    raise SystemExit("oof")
