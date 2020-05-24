import subprocess as sp
import time

from klaxon import klaxon

import pytest

strings = ["What's good?", "hello, klaxon", ""]


@pytest.mark.parametrize("title", strings)
@pytest.mark.parametrize("subtitle", strings)
@pytest.mark.parametrize("message", strings)
def test_klaxon(title, subtitle, message):
    klaxon(title=title, subtitle=subtitle, message=message, sound=None)
    sp.run(
        f"klaxon "
        f'--title "{title}" '
        f'--subtitle "{subtitle}" '
        f'--message "{message}" '
        f'--sound ""',
        shell=True,
    )


def test_klaxon_invoke():
    sp.run(["inv", "successful-task"])
    time.sleep(3)
    sp.run(["inv", "failed-task"])
