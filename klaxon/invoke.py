import functools

from klaxon import klaxon


def klaxonify(func):
    """A special decorator for invoke functions.

    http://www.pyinvoke.org

    usage:

        @task
        @klaxonify
        def my_task(c):
            ...

    """

    @functools.wraps(func)
    def wrapper(c, *args, **kwargs):
        try:
            func(c, *args, **kwargs)
        except Exception as e:
            klaxon(subtitle=f"{func.__name__}", message=f"failed: {repr(e)}")
        else:
            klaxon(subtitle=f"{func.__name__}", message="success")

    return wrapper
