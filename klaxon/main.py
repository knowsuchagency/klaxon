import argparse
import logging
import os
import shlex
import subprocess as sp
import sys
from functools import partial, wraps
from typing import *

from notifiers import get_notifier

from klaxon import config
from klaxon.configuration import get_notifiers_provider_config
from klaxon.exceptions import KlaxonExit

ENABLE_PUSH_NOTIFICATIONS = config.get("enable-notifiers", False)


def klaxon(
    message="",
    title="Klaxon",
    subtitle="",
    sound="",
    push=ENABLE_PUSH_NOTIFICATIONS,
    provider_config_factory=None,
):
    """
    Wraps osascript.

    see https://apple.stackexchange.com/questions/57412/how-can-i-trigger-a-notification-center-notification-from-an-applescript-or-shel/115373#115373
    """

    escaped_message, escaped_title, escaped_subtitle, escaped_sound = [
        shlex.quote(str(e).replace(" ", "-"))
        for e in (message, title, subtitle, sound)
    ]

    if sys.platform == "darwin":
        sp.run(
            shlex.split(
                f"""osascript -e 'display notification "{escaped_message}" with title "{escaped_title}" subtitle "{escaped_subtitle}" sound name "{escaped_sound}"'"""
            )
        )
    else:
        logging.warning(
            "osascript notifications from klaxon only work on Mac OS"
        )

    if push:
        _send_push_notifications(
            message=message,
            title=title,
            subtitle=subtitle,
            provider_config_factory=provider_config_factory,
        )


def klaxonify(
    func=None,
    title="Klaxon",
    message="",
    subtitle=None,
    sound="",
    output_as_message=False,
    push=ENABLE_PUSH_NOTIFICATIONS,
    provider_config_factory=None,
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
        push: send push notification(s)
        provider_config_factory: factory for kwargs that will be passed to `notifiers.notify`

    Returns: decorated function

    """

    def decorator(function):
        @wraps(function)
        def inner(*args, **kwargs):
            result = function(*args, **kwargs)
            klaxon(
                subtitle=subtitle
                if subtitle is not None
                else function.__name__,
                message=message if not output_as_message else result,
                title=title,
                sound=sound,
                push=push,
                provider_config_factory=provider_config_factory,
            )
            return result

        return inner

    if func is not None:
        return decorator(func)
    else:
        return decorator


def _send_push_notifications(
    title,
    subtitle,
    message,
    provider_config_factory: Callable[[str, str, str], dict] = None,
):
    """Send push notifications."""
    try:
        import notifiers
    except (ImportError, ModuleNotFoundError):
        raise KlaxonExit(
            os.linesep.join(
                [
                    "notifiers enabled but not installed",
                    "$ pip(x) install klaxon[notifiers]",
                ]
            )
        )

    if "notifiers" not in config:
        raise KlaxonExit("notifiers key not found in configuration")

    message = message.strip('"').strip("'")

    provider_config = (
        get_notifiers_provider_config(message, subtitle, title)
        if provider_config_factory is None
        else provider_config_factory(message, subtitle, title)
    )

    for provider in config["notifiers"]:
        name = provider.pop("name")

        kwargs = {**provider_config.get(name, {}), **provider}

        if (
            "message" in get_notifier(name).required["required"]
            and "message" not in kwargs
        ):
            kwargs["message"] = message

        notifiers.notify(name, **kwargs)


def main():
    """Parse arguments from command line and pass to notify function."""
    parser = argparse.ArgumentParser(
        prog="klaxon",
        description="Send Mac OS notifications through osascript.",
    )

    parser.add_argument(
        "--message", "-m", default="", help="The body of the notification"
    )

    parser.add_argument(
        "--title", "-t", default="Klaxon", help="The notification's title"
    )

    parser.add_argument(
        "--subtitle", "-s", default="", help="The notification's subtitle"
    )

    parser.add_argument("--sound", help="The sound the notification makes")

    parser.add_argument(
        "--no-push",
        "-n",
        action="store_false",
        help="disable push notifications",
        dest="push",
        default=ENABLE_PUSH_NOTIFICATIONS,
    )

    read_stdin = sys.argv.pop() if sys.argv[-1].strip() == "--" else None

    args = parser.parse_args()

    klaxon_ = partial(
        klaxon,
        title=args.title,
        subtitle=args.subtitle,
        sound=args.sound,
        push=args.push,
    )

    if read_stdin is None:
        klaxon_(args.message)
    else:
        with sys.stdin as fd:
            klaxon_(fd.read())


if __name__ == "__main__":
    main()
