import textwrap
from pathlib import Path
from typing import *

import toml

D = Dict[Any, Any]


def _get_config() -> D:
    """
    Return a dictionary of config values.

    First look in ~/.config/klaxon/config.toml
    Then in [tool.klaxon] in pyproject.toml
    """
    result: D = {}

    default_config_path = Path(Path.home(), ".config", "klaxon", "config.toml")

    if default_config_path.exists():
        result.update(toml.load(default_config_path))

    pyproject_toml_path = Path(Path.cwd(), "pyproject.toml")

    if pyproject_toml_path.exists():
        klaxon_options = toml.load(pyproject_toml_path)
        _recursive_update(
            result, klaxon_options.get("tool", {}).get("klaxon", {})
        )

    return result


def _recursive_update(d1: D, d2: D) -> D:
    """
    Updates d1 with values from d2 as one would expect.
    """
    for key in set(list(d1.keys()) + list(d2.keys())):
        if key in d1 and key in d2:
            if all(isinstance(d[key], dict) for d in (d1, d2)):
                _recursive_update(d1[key], d2[key])
            else:
                d1[key] = d2[key]
        elif key in d2 and key not in d1:
            d1[key] = d2[key]
    return d1


def get_notifiers_provider_config(message, subtitle, title) -> dict:
    """
    Return kwargs that will be passed to `notifiers.notify` method.
    """
    # different providers have different requirements for the `notify` method
    # most seem to take a `message` parameter, but they also have different
    # potential formatting requirements for messages.

    # use the following provider-specific map for `notify` parameters
    provider_config = {
        "pushover": {
            "message": textwrap.dedent(
                f"""
                <i>{subtitle}</i>

                {message}
                """
            ),
            "title": title,
            "html": True,
        },
        "slack": {"message": message if message else "task complete"},
    }
    return provider_config


config = _get_config()
