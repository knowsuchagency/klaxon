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
        success = False
        failed_with_regular_exception = False
        try:
            func(c, *args, **kwargs)
        except Exception as e:
            klaxon(subtitle=f"{func.__name__}", message=f"failed: {repr(e)}")
            failed_with_regular_exception = True
        else:
            klaxon(subtitle=f"{func.__name__}", message="success")
            success = True
        finally:
            if not success and not failed_with_regular_exception:
                klaxon(subtitle=f"{func.__name__}", message=f"failed: catastrophically")

    return wrapper
