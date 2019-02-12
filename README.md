# Klaxon

Send Mac OS notifications from the terminal or Python programs.

This is useful for when you want a push notification 
for some long-running background task.

This is similar to the [terminal-notifier ruby gem][terminal-notifier],
but posix-compliant and with fewer features (PR's welcome).

## Usage

### terminal

```bash
# blank notification
klaxon
# with custom message
klaxon --message "this is the message body"
# pipe message from other program
echo "this is the message body" | klaxon --
```

### python

```python
from klaxon import klaxon, klaxonify

# send a blank notification

klaxon()

# we can decorate our functions to have
# them send notifications at termination

@klaxonify
def hello(name='world'):
    return f'hello, {name}'

@klaxonify(title='oh hai', output_as_message=True)
def foo():
    return "This will be the message body."

```

## Installation
For command-line use, the recommended method of installation is through [pipx].
```bash
pipx install klaxon
```
Naturally, klaxon can also be pip-installed.
```bash
pip install klaxon
```

[terminal-notifier]: https://github.com/julienXX/terminal-notifier
[pipx]: https://github.com/pipxproject/pipx