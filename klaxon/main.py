#!/usr/bin/env python3
from functools import partial, wraps
import subprocess as sp
import argparse
import logging
import shlex
import sys


def klaxon(message: str= '', title="Klaxon", subtitle="", sound=""):
    """
    Wraps osascript.

    see https://apple.stackexchange.com/questions/57412/how-can-i-trigger-a-notification-center-notification-from-an-applescript-or-shel/115373#115373
    """
    if not sys.platform == 'darwin':
        logging.error('klaxon only works on Mac OS')
        return

    message, title, subtitle, sound = map(shlex.quote, (message, title, subtitle, sound))
    command = f"""osascript -e 'display notification "{message}" with title "{title}" subtitle "{subtitle}" sound name "{sound}"'"""
    sp.run(shlex.split(command))


def klaxonify(
    func=None,
    title="Klaxon",
    message="",
    subtitle=None,
    sound="",
    output_as_message=False,
):
    """
    Send a notification at the termination of a function.

    Args:
        func: the function to be decorated
        title: the notification title
        message: the notification message body
        subtitle: the notifiction subtitle
        sound: the notification sound
        output_as_message (bool): use the decorated function's output as the message body

    Returns: decorated function

    """

    def decorator(function):
        @wraps(function)
        def inner(*args, **kwargs):
            result = function(*args, **kwargs)
            klaxon(
                subtitle=subtitle if subtitle is not None else function.__name__,
                message=message if not output_as_message else result,
                title=title,
                sound=sound,
            )
            return result

        return inner

    if func is not None:
        return decorator(func)
    else:
        return decorator


def main():
    """Parse arguments from command line and pass to notify function."""
    parser = argparse.ArgumentParser(
        prog="klaxon", description="Send Mac OS notifications through osascript."
    )

    parser.add_argument("--message", default="", help="The body of the notification")
    parser.add_argument("--title", default="Klaxon", help="The notification's title")
    parser.add_argument("--subtitle", default="", help="The notification's subtitle")
    parser.add_argument("--sound", help="The sound the notification makes")

    read_stdin = sys.argv.pop() if sys.argv[-1].strip() == "--" else None

    args = parser.parse_args()

    klaxon_ = partial(
        klaxon, title=args.title, subtitle=args.subtitle, sound=args.sound
    )

    if read_stdin is None:
        klaxon_(args.message)
    else:
        with sys.stdin as fd:
            klaxon_(fd.read())


if __name__ == "__main__":
    main()
