from invoke import task
from klaxon.invoke import klaxonify


@task
@klaxonify
def successful_task(c):
    ...


@task
@klaxonify
def failed_task(c):
    raise ValueError("derp")
